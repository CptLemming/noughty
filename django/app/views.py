from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import redis
import json

from .models import Comments, Game, GameMove, User

@login_required
def home(request):
    comments = Comments.objects.select_related().order_by('id').all()[0:100]
    
    try:
        current_game = get_current_game(request.user)
    except:
        current_game = {'moves': []}
        
    board = []
    
    for x in range(1,4):
        for y in range(1,4):
            piece = 'none'
            
            for move in current_game['moves']:
                if move['x'] == x and move['y'] == y and move['piece']:
                    piece = move['piece']
                    break
            
            board.append({'model': '{{x_%s_y_%s}}' % (x,y), 'x': x, 'y': y, 'piece': piece})
    
    return render(request, 'index.html', locals())

def angular(request):
    return render(request, 'angular.html')

@csrf_exempt
def node_api(request):
    try:
        # Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)

        # Create Comment
        Comments.objects.create(user=user, text=request.POST.get('comment'))

        # Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('chat', user.username + ': ' + request.POST.get('comment'))

        return HttpResponse("Everything worked :)")
    except Exception, e:
        return HttpResponseServerError(str(e))

def user_info(request):
    try:
        # Get info of currenty logged in user
        data = request.user
        
        return JsonResponse(data={"user_id": data.pk, "username": data.username})
    except Exception, e:
        return HttpResponseServerError(str(e))

@csrf_exempt
def start_game(request):
    try:
        # Player X
        player_x = User.objects.get(id=request.POST.get('player_x', 1))
        
        # Player O
        player_o = User.objects.get(id=request.POST.get('player_o', 2))
        
        # Check a game isn't already started for these players
        lookup = Game.objects.filter(status=Game.get_status('started')).filter(Q(player_x=player_x) | Q(player_o=player_o)).first()
        
        if lookup:
            raise Exception('Game already started')
        
        # Create game
        game = Game.objects.create(player_start=player_x, player_x=player_x, player_o=player_o, status=Game.get_status('started'))
        
        return JsonResponse(message='Game created')
    except Exception, e:
        return HttpResponseServerError(str(e))

@csrf_exempt
def make_move(request):
    try:
        # Position X
        position_x = request.POST.get('position_x')
        
        # Position Y
        position_y = request.POST.get('position_y')
        
        # Lookup current user's game
        game = Game.objects.filter(status=Game.get_status('started')).filter(Q(player_x=request.user) | Q(player_o=request.user)).first()
        
        if not game:
            raise Exception('No open game')
        
        # Calc move number
        move_number = GameMove.objects.filter(game=game).count() + 1
        
        # Check it is this player turn
        if game.player_start == request.user:
            if move_number%2 == 0:
                raise Exception('Not your turn')
        else:
            if move_number%2 == 1:
                raise Exception('Not your turn')
        
        # Check move has not already been made
        lookup = GameMove.objects.filter(game=game, position_x=position_x, position_y=position_y).first()
        
        if lookup:
            raise Exception('Position is taken')
        
        # Make a move
        move = game.game_move.create(player=request.user, position_x=position_x, position_y=position_y, move_number=move_number)
        
        result = 'over' if is_game_over(request.user, game) else 'notover'
        
        return JsonResponse(data={"result": result})
    except Exception, e:
        return HttpResponseServerError(str(e))

def is_game_over(user, game):
    """
    Do something fancy here to determine if the game has ended!
    If the game is over, update the status and set the winner!
    """
    
    ended = False
    
    winning_conditions = (
        ((1,1),(1,2),(1,3)), # Top row
        ((2,1),(2,2),(2,3)), # Middle row
        ((3,1),(3,2),(3,3)), # Bottom row
        ((1,1),(2,1),(3,1)), # Left column
        ((1,2),(2,2),(3,2)), # Middle column
        ((1,3),(2,3),(3,3)), # Right column
        ((1,1),(2,2),(3,3)), # Left top, bottom right diagnal
        ((1,3),(2,2),(3,1)), # Right top, bottom left diagnal
    )
    
    player = []
    opponent = []
    
    if game.game_move.all().count() == 9:
        game.status = game.get_status('draw')
        game.save()
        
        return True
    
    for move in game.game_move.all():
        if (move.player == user):
            player.append((move.position_x, move.position_y))
        else:
            opponent.append((move.position_x, move.position_y))
    
    # Loop over winning conditions, looking for a match
    for cond in winning_conditions:
        if cond[0] in player and cond[1] in player and cond[2] in player:
            ended = True
            break
        
        if cond[0] in opponent and cond[1] in opponent and cond[2] in opponent:
            ended = True
            break
    
    if ended:
        game.winner = user
        game.status = Game.get_status('finished')
        game.save()
        
        return True
    else:
        return False

def abandon_game(request):
    try:
        # Lookup current user's game
        game = Game.objects.filter(status=Game.get_status('started')).filter(Q(player_x=request.user) | Q(player_o=request.user)).first()
        
        if not game:
            raise Exception('No open game')
        
        game.status = Game.get_status('abandoned')
        game.save()
        
        return JsonResponse(message='Game abandoned')
    except Exception, e:
        return HttpResponseServerError(str(e))

def current_game(request):
    try:
        data = get_current_game(request.user)
        
        return JsonResponse(data=data)
    except Exception, e:
        return HttpResponseServerError(str(e))
    
def get_current_game(user):
    # Lookup current user's game
    game = Game.objects.filter(status=Game.get_status('started')).filter(Q(player_x=user) | Q(player_o=user)).first()
    
    if not game:
        raise Exception('No open game')
    
    # Current number of moves
    move_number = GameMove.objects.filter(game=game).count()
    
    moves = []
    
    if game.player_start == user:
        turn = True if move_number%2 is 0 else False
    else:
        turn = True if move_number%2 is 1 else False
        
    is_x = True if game.player_x is user else False
    
    for move in game.game_move.all():
        piece = 'x' if move.player is user else 'y'
        moves.append({'x': move.position_x, 'y': move.position_y, 'piece': piece})
        
    return {'started': True, 'moves': moves, 'players_turn': turn}

def JsonResponse(message=None, data=None, status='success'):
    response_data = {}
    response_data['status'] = status
    
    if message:
        response_data['message'] = message
    
    if data:
        response_data['data'] = data
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
from django.db import models
from django.contrib.auth.models import User


class Comments(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=255)


class Game(models.Model):
    STATUS = (('started','Started'),('finished','Finished'),('abandoned','Abandoned'),('draw','Draw'))
    player_start = models.ForeignKey(User, related_name='game_player_start')
    player_x = models.ForeignKey(User, related_name='game_player_x')
    player_o = models.ForeignKey(User, related_name='game_player_o')
    winner = models.ForeignKey(User, null=True, related_name='game_player_winner')
    status = models.CharField('Game status', choices=STATUS, max_length=255)
    
    @staticmethod
    def get_status(status):
        for s in Game.STATUS:
            if s[0] == status:
                return s[1]


class GameMove(models.Model):
    game = models.ForeignKey(Game, related_name='game_move')
    player = models.ForeignKey(User, related_name='game_move_player')
    move_number = models.IntegerField('Move number', max_length=11)
    position_x = models.IntegerField('Position X', max_length=11)
    position_y = models.IntegerField('Position Y', max_length=11)

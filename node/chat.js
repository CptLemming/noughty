var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');

var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient();

// Sub to the Redis chat channel
sub.subscribe('chat');

// Configure socket.io to store cookie set by Django
io.configure(function(){
    io.set('authorization', function(data, accept){
        if (data.headers.cookie) {
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }

        return accept('error', false);
    });

    io.set('log level', 1);
});

var users = {};

var getSessionId = function(socket) {
    return socket.handshake.cookie['sessionid'];
}

io.sockets.on('connection', function(socket){
    console.log('Connected');
    
    // Grab the connected users details from Django
    getUserInfo(socket);
    
    // Grab message from Redis and send to client
    sub.on('message', function(channel, message){
        socket.send(message);
    });

    // Client is sending message through socket.io
    socket.on('send:message', function(message){
        sendMessageOn(socket, message);
    });
    
    socket.on('disconnect', function(){
        console.log('Disconnected');
        var sessionId = getSessionId(socket);
        var user = users[sessionId];
        
        socket.broadcast.emit('user:left', {
            name: user.username
        });
        
        delete users[sessionId];
    });
    
    // Board related stuffs
    socket.on('board:move', function(data) {
        var parsed = JSON.parse(data);
        
        makeMove(socket, parsed);
    });
});

var sendMessageOn = function(socket, message) {
    var values = querystring.stringify({
        comment: message,
        sessionid: getSessionId(socket),
    });

    var options = {
        host: 'localhost',
        port: 8000,
        path: '/node_api',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': values.length
        }
    };

    // Send message to Django server
    var req = http.get(options, function(res){
        res.setEncoding('utf8');

        // Print out error message
        res.on('data', function(data){
            if (data != 'Everything worked :)') {
                console.log('Message: ' + data);
            }
        });
    });

    req.write(values);
    req.end();
}

var getUserInfo = function(socket) {
    var sessionId = getSessionId(socket);
    var values = querystring.stringify({
        sessionid: sessionId,
    });

    var options = {
        host: 'localhost',
        port: 8000,
        path: '/user_info',
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': values.length,
            'Cookie': 'sessionid='+ sessionId
        }
    };

    // Send message to Django server
    var req = http.get(options, function(res){
        res.setEncoding('utf8');

        // Print out error message
        res.on('data', function(data){
            console.log(data);
            decoded = JSON.parse(data);
            users[sessionId] = decoded.data;
            
            // Let other users know a new user has joined
            socket.broadcast.emit('user:join', {
                name: users[sessionId].username
            });
        });
    });

    req.write(values);
    req.end();
}

var makeMove = function(socket, data) {
    var sessionId = getSessionId(socket);
    var values = querystring.stringify({
        sessionid: sessionId,
        position_x: data.x,
        position_y: data.y
    });

    var options = {
        host: 'localhost',
        port: 8000,
        path: '/make_move',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': values.length,
            'Cookie': 'sessionid='+ sessionId
        }
    };

    // Send message to Django server
    var req = http.get(options, function(res){
        res.setEncoding('utf8');

        // Print out error message
        res.on('data', function(ret){
            console.log('Make Move return', ret);
            
            // Let other user know a move had been made
            // For now target 'all' users, until we can fix this..
            io.sockets.emit('move:made', {
                spoon: 'Spoons',
                position_x: data.x,
                position_y: data.y
            });
        });
    });

    req.write(values);
    req.end();
}

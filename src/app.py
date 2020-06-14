from flask import Flask , render_template , url_for , request
from flask_socketio import SocketIO , emit, leave_room, join_room
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

socketio = SocketIO(app)

rooms = []

@app.route('/índex')
def index():
    nickname = request.args.get('nickname')
    # if nickname in nicknames:
    #     return render_template('home.html')
    
    return render_template('index.html')
    

@app.route('/home')
def home():
    return render_template('home.html')


def message_received(methods = ['GET', 'POST']):
    print('message received')

@socketio.on('message')
def handle_json (json):
    print('mensaje que recivo', json)
    socketio.emit('message', json,callback = message_received)

@app.route('/create-room')
def create_room():
    return render_template('rooms.html')

@socketio.on('connect')
def connect ():
    print ('client is connected')

@socketio.on('join')
def client_join_room(data):
    print( 'data 2' ,data , type(data))
    nickname = data.get('nickname')
    print(nickname)
    room = data.get('room')
    print ('room : ' , room)
    join_room(room)
    if room not in rooms:
        rooms.append(room)
        socketio.emit('new-room',{
            "rooms" : rooms
        })
    print (rooms)
    print(nickname + ' has joined to ' , room)
    socketio.emit('joined', {
        "nickname" : nickname,
        "room":room,
        "rooms" : rooms
    }, room = room)
    


if __name__ == "__main__":
    
    socketio.run(app)
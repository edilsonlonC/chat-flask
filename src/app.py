from flask import Flask , render_template , url_for , request
from flask_socketio import SocketIO , emit, leave_room, join_room
import json
from utilities.utilities import is_room
import sqlite3
import os

db_dir = os.path.join(os.getcwd(),'DB','users.db')
print(db_dir)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'



socketio = SocketIO(app)

rooms = []


@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        print (nickname , password)
        return render_template('register.html')
    if request.method == 'GET':
        return render_template('register.html')






@app.route('/index')
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

def send_message_to_all(data):
    socketio.emit('message',data)

def send_message_to_room(data):
    room = data.get('room')
    socketio.emit('message',data,room=room)

@socketio.on('message')
def handle_json (json):
    print('mensaje que recivo', json)
    message = json.get('data')
    nickname = json.get('nickname')
    room , is_room_verify , message_to_send = is_room(message,rooms)
    
    if (is_room_verify):
        json['data'] = message_to_send
        json['room'] = room
        
        send_message_to_room(json)
    else :
        send_message_to_all(json)
    

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
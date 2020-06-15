from flask import Flask , render_template , url_for , request , redirect , session
from flask_socketio import SocketIO , emit, leave_room, join_room
import json
from utilities.utilities import is_room
import sqlite3 as sql
import os


db_dir = os.path.join(os.getcwd(),'DB','users.db')
print(db_dir)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'



socketio = SocketIO(app)

rooms = []
clients = {}

#test for register

def list_users():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    for r in rows:
        print ('user : ' , r['nickname'], r['pass'])

@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        try:
            nickname = request.form['nickname']
            password = request.form['password']
            with sql.connect("database.db") as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO user (nickname,pass) VALUES (?,?)", (nickname,password))
                con.commit()
                list_users()
                return render_template('login.html')
        except:
            con.rollback()

        
        finally:
            con.close()
        
        return render_template('register.html')
    if request.method == 'GET':
        return render_template('register.html')






@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        try:
            
            nickname = request.form['nickname']
            password = request.form['password']
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM user WHERE nickname = ? AND pass = ?", (nickname,password))
            rows = cur.fetchall()
            if rows:
                session[nickname] = nickname
                return  redirect(url_for('index', nickname=nickname))
            return render_template('login.html')

        except:
            pass

    if request.method == 'GET':
        return render_template('login.html')




@app.route('/index')
def index():
    nickname = request.args.get('nickname')
    if (session.get(nickname)):
        return render_template('index.html')
    return render_template('login.html')

    # if nickname in nicknames:
    #     return render_template('home.html')
    
    
    

@app.route('/logout')
def logout():
    nickname = request.args.get('nickname')
    print(session)
    session.pop(nickname)
    print(session)
    return render_template('login.html')

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


@socketio.on('private-room')
def private_room(data):
    clients[data.get('nickname')] = request.sid
    print(clients)



@socketio.on('private')
def private(data):
    receiver = data.get('receiver')
    sid = clients.get('receiver')
    if (sid):
        socketio.emit('private' , data, room = clients.get(receiver))



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
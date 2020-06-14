
def is_room(message,rooms):
    verify_room = message.split(' ')[0]
    message = message.split(' ')[1::]
    message = ' '.join(message)
    if (verify_room[0] == '/'):
        room = verify_room.split('/')[1]
        if room in rooms: return room ,True,message
    return None , False , message



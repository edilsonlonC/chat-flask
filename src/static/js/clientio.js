let params = location.href.split('?')[1]
let nickname = params.split('=')[1]
let chat = $('#chat');
let message = $('#message')
let boxchat = $('#boxchat')
let roomjoin = $('#roomjoin')
let textroom = $('#textroom')
let listrooms= $('#listrooms')
let linkrooms = $('.linkrooms')

console.log(linkrooms.get(0));


function render_message(data) {
    console.log('test in render');

    if (data.nickname === nickname)
        boxchat.append(`<span> desde main me :  ${data.data} <span> <br>`)
    else
       boxchat.append(`<span> ${data.nickname} :  ${data.data} <span> <br>`)

}

function render_rooms(rooms){

    let string_to_rooms = ``
    for(var i = 0; i < rooms.length; i++){
        string_to_rooms += `<a href="javascript:void(0)" class="linkrooms"> ${rooms[i]} </a> <br>`
    }
    console.log(string_to_rooms);
    
    listrooms.html(string_to_rooms)


}
function main()
{

var socket = io();
socket.on('connect', function () {

    chat.submit(function (e) {
        e.preventDefault()
        let message_to_send = message.val()
        socket.emit('message', {
            data: message_to_send,
            nickname
        })
        message.val('')
        
    })
    socket.on('message', data => {
        console.log(data);
        render_message(data)
    })

   
    roomjoin.submit( e=> {
        e.preventDefault()
        let room = textroom.val()
        if (room.trim().length === 0) return
        socket.emit('join',{
            nickname,
            room
        })
    })

   

    socket.on('joined', data => {
        console.log(data)
        
    })
    socket.on('new-room', data => {
      
        render_rooms(data.rooms)
        
    })

})
}

main()
let params = location.href.split('?')[1]
let nickname = params.split('=')[1]
let chat = $('#chat');
let message = $('#message')
let boxchat = $('#boxchat')
let roomjoin = $('#roomjoin')
let textroom = $('#textroom')
let listrooms= $('#listrooms')
let linkrooms = $('button')
let lastroom = ''

console.log(linkrooms);
console.log('holi');


function render_message(data) {
    console.log(data);
    if(data.room){
        boxchat.append(`<span class="bg-info text-white font-weight-bold"> ${data.room} </span>`)
    }   else{
        lastroom = ''
    }
    if (data.nickname === nickname)
        boxchat.append(`<span class="text-white font-weight-bold"> yo:  ${data.data} <span> <br>`)
    else
       boxchat.append(`<span> ${data.nickname} :  ${data.data} <span> <br>`)
    boxchat.scrollTop(boxchat[0].scrollHeight)
}

function render_rooms(rooms){
    var vista_rooms = '<h2 class="mt-3 ml-3 text-white">' +
                    'SALAS' +
                '</h2>' +
                '<div class="rooms-container-create text-center ml-3">' +
                    '<!-- join and create room-->' +
                    '<form class="form-inline" id="roomjoin" action="javascript:void(0)">' +
                        '<div class="form-group">' +
                            '<label for="textroom" class="sr-only">Nombre sala</label>' +
                            '<input class="form-control col-sm" id="textroom" type="text" placeholder="Nombre sala">' +
                        '</div>' +
                        '<button class="btn btn-success" type="submit">Ingresar</button>' +
                        '<!-- <input class="btn btn-success" type="submit" value="join room"> -->' +
                    '</form>' +
                '</div>';
    var encabezado = '<br><div class="btn-group-vertical ml-3" role="group" aria-label="Basic example">';
    var pie = '</div>';
    let string_to_rooms = ``
    for(var i = 0; i < rooms.length; i++){
        string_to_rooms += `<button class="btn btn-primary" onclick='room_autocomp("${rooms[i]}")'> ${rooms[i]} </button>`
    }
    console.log(string_to_rooms);
    
    listrooms.html(vista_rooms+encabezado+string_to_rooms+pie)
}

function room_autocomp(room){
    lastroom = '/' + room + ' '
    message.val(lastroom)
}

function iniciar_sesion(){
    $('#registro').hide();
    $('#inicio_sesion').show();
}

function registrarse(){
    $('#inicio_sesion').hide();
    $('#registro').show();
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
        message.val(lastroom)
        
    })

    /*linkrooms.click(function(){
        alert('click')
    })*/
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
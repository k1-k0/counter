fetch('/increment').then(function(response) {
    return response.json();
}).then(function (data) {
    document.body.innerHTML = data;
})

const socket = new WebSocket('ws://localhost:8080/ws');

socket.addEventListener('open', function (event) {
    socket.send('Hello server!');
})

socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
    document.body.innerHTML = event.data;
})
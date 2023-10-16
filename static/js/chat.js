const id = JSON.parse(document.getElementById("json-username").textContent)
const message_username = JSON.parse(document.getElementById("json-message-username").textContent)
// He is sending the message, username of the logged in user.
const reciever = JSON.parse(document.getElementById("json-username-receiver").textContent)
// He is recieving the message


const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function(e){
    console.log("connection established")
}

socket.onclose = function(e){
    console.log(e)
    console.log("connection Closed Again")
}

socket.onerror = function(e){
    console.log(e)
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data)
    console.log(data)

    //data.username is the username of the person who is sending the data
    //message_username is the username of the person who is logged in.
    //So if both are same and the person sends message it should be showed in the right
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `
        <tr>
            <td>
                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                   ${data.message}
                </p>
            </td>
        </tr>
       `
    }
    //if above condition is false we need to render the message on the left side instead of right
    // float-left instead of flot-right as above
    else{
        document.querySelector('#chat-body').innerHTML += `
        <tr>
            <td>
                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
                   ${data.message}
                </p>
            </td>
        </tr>
       `
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    // console.log(message_input)
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message' : message,
        'username' : message_username,
    }))

    message_input.value = '';
    
}
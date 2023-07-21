'use strict';
/**
* @module       frontend: cross-site-scripting
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Directory traversal page demonstration logic.
*/

/**
 * Backend API URL
 * @const
 */
const API_URL  = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

/**
 * Security measure for client side flag variable.
 * @var
 */
var secure_client = false;

/**
 * Security measure for server side flag variable.
 * @var
 */
var secure_server = false;

/**
 * Request all messages for current session and display them in the chat window.
 */
async function fetch_messages() {
    var res = await fetch(API_URL + "/chatting", {
        method: 'GET',
        credentials: 'include',
    });
    
    if (res) {
        let chat = await res.json();
        refresh_chat(chat);
    }
}

/**
 * Send message from user as JSON to /chatting endpoint.
 */
async function send_message() {
    var form = document.getElementById("chat-form");
    if (form["username"].value == '' || form["message"].value == '') return;
    
    let payload = {};
    payload[form["username"].value] = form["message"].value;
    var res = await fetch(API_URL + `/chatting?secure=${secure_server}`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    });

    if (res) {
        let chat = await res.json();
        refresh_chat(chat);
    }
    
    // clear message input element
    form["message"].value = '';
}

/**
 * Refresh chat window with messages given by chat parameter.
 * @param {Array} chat Array of messages.  
 */
function refresh_chat(chat) {
    let window = document.getElementById("chat-window");
    while (window.firstChild) { // remove all messages from chat window
        window.removeChild(window.lastChild);
    }

    for (let message of chat) {
        let username = Object.keys(message)[0];
        
        let container = document.createElement('div');
        container.classList = 'chat item';

        // insert in a secure way if enabled
        if (secure_client) {
            let span = document.createElement('span');
            span.classList = 'item-username';
            span.innerText = username + ':';

            let msg = document.createElement('text');
            msg.innerText = message[username];

            container.appendChild(span);
            container.appendChild(msg);
            window.appendChild(container);
            continue;
        }

        // insert in a insecure way otherwise
        container.innerHTML = "<span class='item-username'>" + username + ":</span>" + message[username];
        window.appendChild(container);
    }
}

/**
 * Send request to /chatting/reset endpoint which will delete all messages from database
 * and set default messages.
 */
async function clear_chat() {
    var res = await fetch(API_URL + "/chatting/reset", {
        method: 'GET',
        credentials: 'include'
    });
    if (res) {
        let chat = await res.json();
        refresh_chat(chat);
    }
}

/**
 * Toggle client side security measure.
 */
function toggle_client_side_security() {
    secure_client = document.getElementById("enable-security-client").classList.contains('checked');
}

/**
 * Toggle server side security measure.
 */
function toggle_server_side_security() {
    secure_server = document.getElementById("enable-security-server").classList.contains('checked');
}
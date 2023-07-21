'use strict';
/**
* @module       backend: chatting-service
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Implementation of chatting services.
*/
const db = require('./internal.db.service');

/**
 * Get all messages from the chat room associated with given session id.
 * @param {String} session Session id.
 * @returns Entire chat room message history.
 */
async function getAll(session){
    let messages = await db.getAll("ChatRooms", session);
    return messages;
}

/**
 * Insert new message to the chat room associated with given session id.
 * @param {String} session Session id.
 * @param {Object} message Message in {"username": "message"} format.
 * @param {Boolean} secure  Flag indicating whether request should be processed in a secure way or not.
 * @returns Updated chat room message history.
 */
async function insert(session, message, secure=false){
    // escape HTML characters if secure processing is enabled
    if (secure) {
        let msg = message[Object.keys(message)[0]];
        message[Object.keys(message)[0]] = escapeRiskyCharacters(msg);
    }
    return await db.insert("ChatRooms", session, message);
}

/**
 * Reset messages in the chat room associated with given session id into default preset. 
 * @param {String} session Session id. 
 * @returns Updated (set to default) message history of the chat room.
 */
async function reset(session) {
    let messages = await db.reset("ChatRooms", session);
    return messages;
}

/**
 * Escape all HTML characters in given text to prevent code interpretation by the browser.
 * @param {String} text Text which should be escaped from HTML tag characters.
 * @returns Text with escaped HTML characters. 
 */
function escapeRiskyCharacters(text) {  
    let risky_chars = {"<": "&lt;", ">": "&gt;","&": "&amp;", "\"": "&quot;"};                      
    return text.replace(/[<>&"]/g, function(char) {  
        return risky_chars[char];  
    }); 
}

module.exports = {
  getAll,
  insert,
  reset
}
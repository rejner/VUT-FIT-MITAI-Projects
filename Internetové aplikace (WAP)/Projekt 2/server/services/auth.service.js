'use strict';
/**
* @module       backend: auth-service
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Implementation of authentication services.
*/
const db = require('./internal.db.service');

/**
 * Authenticate user, generate security token and link
 * session to logged in user. 
 * @param {String} username User's username.
 * @param {String} password User's password.
 * @param {String} session  Session id.
 * @returns User's credentials with security token.
 */
async function logIn(username, password, session){
    let user = await db.get("Users", session, username);
    if (user && user["password"] === password) {
        let token = Math.floor(Math.random() * 4096);
        user["token"] = token;
        await db.reset("UsersOnline", session);
        await db.insert("UsersOnline", session, {"token": token, "id": user["id"]});
        return user;
    } 
    throw Error("Incorrect password!");
}

/**
 * Reset link with session and logged in user.
 * @param {String} session Session id.
 */
async function logOut(session){
    await db.reset("UsersOnline", session);
}

module.exports = {
    logIn,
    logOut
}
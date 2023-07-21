'use strict';
/**
* @module       backend: chatting-controller 
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Chatting route controller.
*/
const chat = require('../services/chatting.service');

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Get all messages in the chat room.
 */
async function getAll(req, res, next) {
    console.log("Name: " + "ChatRooms" + ", Session: " + req.sessionID);
    try {
        res.json(await chat.getAll(req.sessionID));
    } catch (err) {
        console.error(`Error while getting chatting rooms`, err.message);
        next(err);
    }
}

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Insert new entry into chat room.
 */
async function insert(req, res, next) {
    try {
        res.json(await chat.insert(req.sessionID, req.body, req.query.secure === "true"));
    } catch (err) {
        console.error(`Error while creating chatting room`, err.message);
        next(err);
    }
}

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Clear all messages from the chat room and set default.
 */
async function reset(req, res, next) {
    console.log("Chat reset command received.");
    try {
        res.json(await chat.reset(req.sessionID));
    } catch (err) {
        console.error(`Error while reseting chatting room`, err.message);
        next(err);
    }
}

module.exports = {
    insert,
    getAll,
    reset
};
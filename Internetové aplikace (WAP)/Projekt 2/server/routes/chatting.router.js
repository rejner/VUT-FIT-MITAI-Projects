'use strict';
/**
* @module       backend: chatting-router
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Chat router endpoints definition.
*/
const express = require('express');
const router = express.Router();
const chattingController = require('../controllers/chatting.controller');

/**
 * Get entire chat room message history.
 * @name Get message history.
 * @route {GET} /chatting
 */
router.get('/', chattingController.getAll);
  
/**
 * Send message and append it to the chat history
 * @name Send message.
 * @route {POST} /chatting
 * @bodyparam {Object} JSON object in {"username": "message"} format.
 * @queryparam {String} [secure] Flag which activates security measure.
 */
router.post('/', chattingController.insert);

/**
 * Reset entire chat room message history.
 * @name Reset message history.
 * @route {GET} /chatting/reset
 */
router.get('/reset', chattingController.reset);

module.exports = router;
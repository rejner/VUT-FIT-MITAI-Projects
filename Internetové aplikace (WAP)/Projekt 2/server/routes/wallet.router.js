'use strict';
/**
* @module       backend: wallet-router
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Wallet router endpoints definition.
*/
const express = require('express');
const router = express.Router();
const walletController = require('../controllers/wallet.controller');

/**
 * Get balance of specified user.
 * @name Get balance.
 * @route {GET} /wallet/balance/:id
 * @routeparam {String} :id User's id;
 */
router.get('/balance/:id', walletController.getBalance);

/**
 * Send funds to another user.
 * @name Send funds.
 * @route {POST} /wallet/send
 * @bodyparam {Object} JSON object with fields:
 * @bodyparam {String} fromId Id of user who is sending funds.
 * @bodyparam {String} toId Id of user who is receiving funds.
 * @bodyparam {String} value Value to be sent.
 * @bodyparam {String} token Validation token (required if "secure" is set).
 * @bodyparam {String} secure Enable security measure (token validation) "true"|"false".
 */
router.post('/send', walletController.send);

module.exports = router;
'use strict';
/**
* @module       backend: auth-router
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Authentication router endpoints definition.
*/
const express = require('express');
const router = express.Router();
const authController = require('../controllers/auth.controller');

/**
 * @name Log in user.
 * @route {POST} /auth/login
 * @bodyparam {String} username User's username.
 * @bodyparam {String} password User's password.
 */
router.post('/login', authController.logIn);

/**
 * @name Log out user.
 * @route {GET} /auth/logout
 * @description Log out operation is performed based on session id.
 */
router.get('/logout', authController.logOut);

module.exports = router;
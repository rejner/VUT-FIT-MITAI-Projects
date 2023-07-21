'use strict';
/**
* @module       backend: files-router
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Files router endpoints definition.
*/

const express = require('express');
const router = express.Router();
const filesController = require('../controllers/files.controller');

/**
 * @name Read file .
 * @route {GET} /files/read
 * @queryparam {String} [file] Path of required file.
 * @queryparam {String} [secure] Flag which activates security measure.
 */
router.get('/read', filesController.readFile);

module.exports = router;
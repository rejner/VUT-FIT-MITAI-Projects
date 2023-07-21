'use strict';
/**
* @module       backend: files-controller 
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Files route controller.
*/

const files = require('../services/files.service');

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Read file specified as URL query parameter.
 */
async function readFile(req, res, next) {
    console.log("File: " + req.query.file + ", Session: " + req.sessionID);
    try {
        let data = await files.readFile(req.query.file, req.query.secure === "true");
        res.send(data);
    } catch (err) {
        console.error(`Error while reading file: `, err.message);
        res.status(404).send(err.message);
    }
}

module.exports = {
    readFile
};
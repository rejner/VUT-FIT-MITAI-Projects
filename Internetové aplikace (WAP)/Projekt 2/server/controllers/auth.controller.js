'use strict';
/**
* @module       backend: auth-controller 
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Authentication route controller.
*/
const auth = require('../services/auth.service');

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Authenticates and logs in user if successful.
 */
async function logIn(req, res, next) {
    console.log("Auth login" + ", Session: " + req.sessionID);
    try {
        res.json(await auth.logIn(req.body["username"], req.body["password"], req.sessionID));
    } catch (err) {
        res.status(400).send("Given credentials don't match!");
    }
}

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Logs out user.
 */
async function logOut(req, res, next) {
    console.log("Auth logout" + ", Session: " + req.sessionID);
    try {
        await auth.logOut(req.sessionID);
        res.status(200).send("Success!");
    } catch (err) {
        res.status(400).send(err.message);
    }
}

module.exports = {
    logIn,
    logOut
};
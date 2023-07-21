'use strict';
/**
* @module       backend: wallet-controller 
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Wallet route controller.
*/
const wallet = require('../services/wallet.service');

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Get wallet balance of logged in user.
 */
async function getBalance(req, res, next) {
    console.log("Wallet getBalance" + ", Session: " + req.sessionID);
    try {
        res.json(await wallet.getBalance(req.params.id, req.sessionID));
    } catch (err) {
        console.error(`Error while getting balance: `, err.message);
        res.status(401).send("Permission denied.");
    }
}

/**
 * @param {Request} req         Request object
 * @param {Response} res        Response object 
 * @param {NextFunction} next   Next function object
 * @description Send value from user's wallet to another user's account.
 */
async function send(req, res, next) {
    console.log("Wallet send" + ", Session: " + req.sessionID);
    try {
        res.json(await wallet.send(req.body["fromId"], req.body["toId"], req.body["value"], req.sessionID, req.body["token"], req.body["secure"] === "true"));
    } catch (err) {
        console.error(`Error while sending money: `, err.message);
        res.status(401).send("Permission denied.");
    }
}

module.exports = {
    getBalance,
    send
};
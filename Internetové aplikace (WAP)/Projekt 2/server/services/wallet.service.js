'use strict';
/**
* @module       backend: wallet-service
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Implementation of wallet service.
*/
const db = require('./internal.db.service');

/**
 * Get account information of the wallet with given id.
 * @param {String} id Id of the wallet. 
 * @param {String} session Id of user's session.
 * @returns Record with account information with id specified by parameter.
 */
async function getBalance(id, session) {
    // check if user was authenticated recently and is linked to current session
    let auth = await db.get("UsersOnline", session, id);
    if (auth) {
        let res = await db.get("Wallets", session, id);
        console.log(`Retrieving balance of ${id}, balance: ${res["balance"]}`);
        return res;
    }
    throw Error("Authentication error!");
}

/**
 * Send funds from one wallet to another.
 * @param {String} from     Id of the source wallet.
 * @param {String} to       Id of the destination wallet.
 * @param {String} value    Value to be sent.
 * @param {String} session  Id of user's session who is performing transaction.
 * @param {String} token    Validation token.
 * @param {Boolean} secure  Flag indicating whether request should be processed in a secure way or not.
 * @returns Updated record with account information of the sender.
 */
async function send(from, to, value, session, token=null, secure=false) {
    // check if user was authenticated recently and is linked to current session
    let auth = await db.get("UsersOnline", session, from);
    if (auth) {
        if (secure && !(token == auth["token"])) throw Error("Token missmatch!");
        // check if user has enough funds
        let fromUser = await db.get("Wallets", session, from);
        let toUser = await db.get("Wallets", session, to);
        let fromUserAmount = parseFloat(fromUser["balance"]) - parseFloat(value);
        let toUserAmount = parseFloat(toUser["balance"]) + parseFloat(value);

        if (parseFloat(fromUser["balance"]) < value) throw Error("Insufficient funds!");
        let res = await db.update("Wallets", session, from, "balance", fromUserAmount);
        await db.update("Wallets", session, to, "balance", toUserAmount);
        return res;
    }
    throw Error("Authentication error!");
}

module.exports = {
    getBalance,
    send
}
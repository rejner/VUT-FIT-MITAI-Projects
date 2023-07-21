'use strict';
/**
* @module       backend: database-service
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Implementation of internal database service.
*/

/**
 * @type {Object}
 * @description Internal multipurpose database object structured as db["database name"]["session id"]["content"]
 */
var db = {
    "ChatRooms" : {
        "default": 
        [
            {"Alice": "Hello Bob!"},
            {"Bob": "Hey Alice!"}
        ]
    },

    "Users"     : {
        "default": 
        [
            {
                "id"      : "Bob",
                "password": "1234"
            },
            {
                "id"      : "Alice",
                "password": "1234"
            },
            {
                "id"      : "Eve",
                "password": "1234"
            },
        ]
    },

    "UsersOnline" : {
        "default":
        [
            /*{
                "token" : "silly_token",
                "id": "some id"
            }*/
        ]
    },

    "Wallets" : {
        "default":
        [
            {
                "id"      : "Bob",
                "balance" : 100.0,
            },
            {
                "id"      : "Alice",
                "balance" : 0.0,
            },
            {
                "id"      : "Eve",
                "balance" : 0.0,
            },
        ]
    }   
}

/**
 * Get all records from the database.
 * @param {String} db_name Database name. 
 * @param {String} session Session id. 
 * @returns All records from database indentified by it's name and session id.
 */
async function getAll(db_name, session) {
    checkExistence(db_name, session);
    return db[db_name][session];
}

/**
 * Get single record from the database.
 * @param {String} db_name Database name. 
 * @param {String} session Session id. 
 * @param {String} id Id of required record.
 * @returns Record specified by it's id.
 */
async function get(db_name, session, id) {
    checkExistence(db_name, session);
    let record = db[db_name][session].find(x => x["id"] === id);
    if (!record) throw Error("There is no record with id " + id + " in the " + db_name +" database!");
    return record;
}

/**
 * Insert new record into the database.
 * @param {String} db_name Database name. 
 * @param {String} session Session id. 
 * @param {*} value New value for insertion. 
 * @returns Updated records of database.
 */
async function insert(db_name, session, value) {
    checkExistence(db_name, session);
    db[db_name][session].push(value);
    return db[db_name][session];
}

/**
 * Update record (key-value pair of specific object) in the database.
 * @param {String} db_name Database name. 
 * @param {String} session Session id. 
 * @param {String} id Id of record which should be updated.
 * @param {*} key Name of the key attribute.
 * @param {*} value New value of the given key attribute.
 * @returns Single updated record.
 */
async function update(db_name, session, id, key, value) {
    checkExistence(db_name, session);
    let record = db[db_name][session].find(x => x["id"] === id);
    if (!record) throw Error("There is no record with id " + id + " in the " + db_name +" database!");
    record[key] = value;
    return record;
}

/**
 * Reset database given it's name and session id to default values specified by "default" session key.
 * @param {String} db_name Database name. 
 * @param {String} session Session id. 
 * @returns Database content set to default values.
 */
async function reset(db_name, session) {
    checkExistence(db_name, session);
    console.log("BEFORE, session: " + session);
    console.log(db[db_name][session]);
    db[db_name][session] = JSON.parse(JSON.stringify(db[db_name]["default"]));
    console.log("AFTER");
    console.log(db[db_name][session]);
    return db[db_name][session];
}

/**
 * Check if database with given name and session exists.
 * If current session wasn't instanciated in the database yet, create new instance with default preset. 
 * @param {String} db_name Database name. 
 * @param {String} session Session id. 
 */
function checkExistence(db_name, session) {
    var context = db[db_name];
    if (!context) {
        throw Error("Database " + db_name + " doesn't exist!");
    }
    var res = context[session];
    if (!res) {
        context[session] = JSON.parse(JSON.stringify(db[db_name]["default"]));
    }
}

module.exports = {
    getAll,
    get,
    update,
    insert,
    reset
}
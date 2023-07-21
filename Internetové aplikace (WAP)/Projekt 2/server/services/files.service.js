'use strict';
/**
* @module       backend: files-service
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Implementation of files services.
*/
const fs = require('fs');
var path = require('path');

/**
 * @constant
 * @type {String}
 * @description Path to root directory of virtual filesystem.
 */
const PSEUDO_ROOT_DIR = "server/container/"
/**
 * @constant
 * @type {String}
 * @description Path to directory with demonstration files.
 */
const FILES_DIR = "wwwroot/data/ice-cream/"

/**
 * Read contents of the file specified by filename parameter.
 * @param {String} filename Name of required file.
 * @param {Boolean} secure  Flag indicating whether request should be processed in a secure way or not.
 * @returns File contents in raw format.
 */
async function readFile(filename, secure=false){
    let final_path = path.join(PSEUDO_ROOT_DIR, FILES_DIR, filename);
    // make sure user can't access anything beyond server/container/ directory (only simulated fs is accessible)
    if (!final_path.startsWith(path.join(PSEUDO_ROOT_DIR))) throw Error("Access violation! (out of filesystem)");
    if (secure) {
        if (!final_path.startsWith(path.join(PSEUDO_ROOT_DIR, FILES_DIR))) throw Error("Access violation! (triggered by security measure)");
    }
    // try to read data
    try {
        const data = fs.readFileSync(final_path, 'utf8');
        return data;
    } catch (err) {
        throw Error("Couldn't read data.");
    }
}


module.exports = {
    readFile
}
'use strict';
/**
* @module       frontend: directory-traversal
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Directory traversal page demonstration logic.
*/

/**
 * Backend API URL
 * @const
 */
const API_URL  = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/files/read?file=`;

/**
 * Security measure flag variable.
 * @var
 */
var secure = false;

/**
 * Update request visualization URL with new input value.
 * @param {String} id Input element id. 
 */
function update_url(id) {
    let file = document.getElementById(id);
    let url_file_path = document.getElementById("traversal-file");
    url_file_path.innerText = file.value;
}

/**
 * Send request to /files/read endpoint with file query parameter.
 */
async function send_request() {
    let file_path = document.getElementById("file-input");
    var res = await fetch(API_URL + file_path.value + `&secure=${secure}`, {
        method: 'GET',
        credentials: 'include'
    });
    if (res) {
        let contents = await res.text();
        document.getElementById("traversal-message").innerText = contents;
    }
}

/**
 * Toggle security measure (set security flag variable which is being sent together with requests).
 */
function toggle_security() {
    secure = document.getElementById("enable-security").classList.contains('checked');
}
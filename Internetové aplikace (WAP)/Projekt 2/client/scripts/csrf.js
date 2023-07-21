'use strict';
/**
* @module       frontend: cross-site-request-forgery
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Cross-site request forgery page demonstration logic.
*/

/**
 * Backend API URL
 * @const
 */
const API_URL  = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
/**
 * URL of malicious site which performs CSRF attack.
 * @const
 */
const EVIL_URL  = `${window.location.protocol}//${window.location.hostname}:7287/demos/evil_site.html`;

/**
 * Send log in request to API. Credentials are extracted from authentication form, request
 * is forged and based on the result either wallet form or error message is shown.
 */
async function log_in() {
    // extract credentials from authentication form
    var form = document.getElementById("auth-form");
    if (form["username"].value == '' || form["password"].value == '') {
        show_error("auth-error-message", "Username or password not provided!");
        return;
    }
    
    let payload = {};
    payload["password"] = form["password"].value;
    payload["username"] = form["username"].value;

    // forge and send request
    var res = await fetch(API_URL + "/auth/login", {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    });

    if (res) {
        // authentication error
        if (res.status === 400) {
            show_error("auth-error-message", "Given credentials don't match!");
            return;
        }
        
        // clear authentication form
        form["username"].value == '';
        form["password"].value == '';
        form.style.display = 'none';

        // display 'Click me!' button
        var evil_btn = document.getElementById("evil-btn");
        evil_btn.style.display = 'flex';

        // read user account information, fill and show wallet form
        let user = await res.json();
        var wallet = document.getElementById("wallet-form");
        wallet.style.display = 'flex';
        wallet.setAttribute("token", user["token"]); // set validation token as attribute 

        let data = await get_balance(user["id"]);
        document.getElementById("wallet-id").value = user["id"];
        document.getElementById("wallet-balance").value = `${data["balance"]} BTC`;
    }
}

/**
 * Perform log out request. Link of logged in user and current session is being disconnected.
 */
async function log_out() {
    var res = await fetch(API_URL + "/auth/logout", {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    if (res) {
        console.log("User logged out.");
        reset_ui();
    }
}

/**
 * Set UI to default state.
 */
function reset_ui() {
    document.getElementById("evil-btn").style.display = 'none';
    
    let wallet = document.getElementById("wallet-form");
    wallet.style.display = 'none';
    wallet.reset();

    let auth = document.getElementById("auth-form");
    auth.style.display = 'flex';
    auth.reset();
    
}

/**
 * Send request to get information about user's account balance.
 * @param {String} id User's id.
 * @returns Object with account information.
 */
async function get_balance(id) {
    var res = await fetch(API_URL + `/wallet/balance/${id}`, {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    if (res) {
        return await res.json();
    }
}

/***
 * Send funds to Alice.
 */
async function send_funds() {
    var form = document.getElementById('wallet-form');
    var enable_sucurity = document.getElementById('enable-security');
    if (form["amount"].value == '') {
        show_error("wallet-error-message", "Enter amount to be sent.");
        return;
    }

    var res = await fetch(API_URL + `/wallet/send`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                "fromId": document.getElementById("wallet-id").value,
                "toId"  : "Alice",
                "value" : form["amount"].value,
                "token" : form.getAttribute('token'),
                "secure": enable_sucurity.classList.contains('checked')})
    });
    if (res) {
        let data = await res.json();
        document.getElementById("wallet-balance").value = `${data["balance"]} BTC`;
    }
}

/**
 * Open evil site which performs attack on EVIL_URL.
 */
async function go_to_evil_site() {
    setTimeout( async () => {
        let user = document.getElementById("wallet-id").value;
        let data = await get_balance(user);
        console.log(data);
        document.getElementById("wallet-balance").value = `${data["balance"]} BTC`;
        document.getElementById("explanation").style.display = 'flex';
        }, 2000);
    window.open(EVIL_URL + `?secure=${document.getElementById("enable-security").classList.contains('checked')}`, '_blank');
}

/**
 * Set error message.
 */
async function show_error(elemId, msg) {
    const error_msg = document.getElementById(elemId);
    error_msg.innerText = msg;
    error_msg.style.display = 'flex';
}
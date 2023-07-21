'use strict';
/**
* @module       frontend: clickjacking
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Clickjacking page demonstration logic.
*/

/**
 * Demonstration site URL which is loaded by iframe window.
 * @const
 */
const SITE_URL  = `${window.location.protocol}//${window.location.hostname}:7287`;

/**
 * Construct final URL (with color mode) and inject iframe into DOM.
 */
function init_iframe() {
    let handle = document.getElementById("iframe-handle");
    let is_dark = sessionStorage.getItem('is_dark');
    if (is_dark === null) is_dark = true;
    handle.innerHTML = `<iframe id="social-post-iframe" secure="false" src="${SITE_URL}/demos/sm_post.html?secure=false&dark=${is_dark}"></iframe>`
    document.getElementById("explanation").style.display = 'flex';
}

/**
 * Toggle overlay buttons (fake buttons) highlighting.
 */
function toggle_hightlight_buttons() {
    let btns = document.getElementsByClassName('social button fake');
    for (let elem of btns) {
        elem.classList.toggle('red');
    }
}

/**
 * Toggle fake overlay display (visibility).
 */
function toggle_disable_overlay() {
    document.getElementById("overlay").classList.toggle('none');
}

/**
 * Toggle observer creation (security measure on target site). New URL has to be created with
 * new parameters and iframe reload is performed.
 */
function toggle_observer() {
    let iframe = document.getElementById("social-post-iframe");
    if (iframe.getAttribute('secure') === "false") {
        iframe.setAttribute('secure', 'true');        
    } else {
        iframe.setAttribute('secure', 'false');
    }
    let is_dark = sessionStorage.getItem('is_dark');
    if (is_dark === null) is_dark = true;
    iframe.setAttribute('src', `${SITE_URL}/demos/sm_post.html?secure=${iframe.getAttribute('secure')}&dark=${is_dark}`);
    iframe.contentWindow.location.reload();
}
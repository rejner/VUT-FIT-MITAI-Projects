'use strict';
/**
* @module       frontend: ui
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  General user interface logic.
*/

/**
 * Dark color mode preset (CSS variables)
 * @const
 */
const dark_mode = {
    '--bg-color': "#262629",
    '--headline-color': "#1bdd25",
    '--text-color': "#7ad430",
    '--select-color': "#ffffff",
}

/**
 * Light color mode preset (CSS variables)
 * @const
 */
const light_mode = {
    '--bg-color': "#F1F1E3",
    '--headline-color': "#262629",
    '--text-color': "#262629",
    '--select-color': "#262629"
}

/**
 * Load selected color mode.
 */
function load_color_mode() {
    let is_dark = sessionStorage.getItem('is_dark') !== null ? sessionStorage.getItem('is_dark') === 'true' : true;
    let mode = is_dark ? dark_mode : light_mode;
    for (var key in mode) {
        document.documentElement.style.setProperty(key, mode[key]);
    }
    var color_mode_btn = document.getElementById('color-mode-btn');
    if (color_mode_btn) {
        color_mode_btn.innerText = is_dark ? "Light mode" : "Dark mode";
    }
}

/**
 * Toggle color mode (light/dark).
 */
function switch_color_mode() {
    var is_dark = sessionStorage.getItem('is_dark') !== null ? sessionStorage.getItem('is_dark') === 'true' : true;
    sessionStorage.setItem('is_dark', !Boolean(is_dark));
    load_color_mode();
}

/**
 * Toggle visibility of the sibling element (used for clickable list items).
 * @param {String} id Element id.
 */
function toggle_description(id) {
    var item_elem = document.getElementById(id);
    var description = item_elem.nextElementSibling;
    console.log(description.style.display);
    description.style.display = (description.style.display === 'none' || description.style.display === '') ? 'flex' : 'none';
    console.log(description.style.display);
}

/**
 * Toggle custom checkbox visual.
 * @param {String} id Element id. 
 */
function toggle_checkbox(id) {
    var el = document.getElementById(id);
    el.classList.toggle('checked');
}
'use strict';
/**
* @module       frontend: social-media-post
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Social media post site logic.
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

// set default counts to local storage
localStorage.setItem('likes', 42);
localStorage.setItem('dislikes', 5);

/**
 * Flag whether block action events or not, set by intersection observer (when enabled) 
 * @var
 */
var block_actions = false;

/**
 * Parse URL query parameters, init styles and create observer if enabled.
 */
function site_init() {
    const query = window.location.search;
    const params = new URLSearchParams(query);
    if (params.get('secure') === "true") create_observer();

    const is_dark = (params.get('dark') === "true");
    let mode = is_dark ? dark_mode : light_mode;
    for (var key in mode) {
        document.documentElement.style.setProperty(key, mode[key]);
    }
}

/**
 * Update elements displaying like/dislike counts.
 */
function update_reactions() {
    let likes = localStorage.getItem('likes');
    let dislikes = localStorage.getItem('dislikes');
    document.getElementById("reactions").innerHTML = 
    `<span>${likes} likes</span>
     <span>${dislikes} dislikes</span>`;
}

/**
 * Perform like press action, increment counter.
 */
function press_like() {
    if (block_actions) return;
    console.log("++");
    let likes = parseInt(localStorage.getItem('likes'));
    likes += 1;
    localStorage.setItem('likes', likes);
    update_reactions();
}

/**
 * Perform dislike press action, increment counter.
 */
function press_dislike() {
    if (block_actions) return;
    console.log("--");
    let dislikes = parseInt(localStorage.getItem('dislikes'));
    dislikes += 1;
    localStorage.setItem('dislikes', dislikes);
    update_reactions();
}

/**
 * Create intersection observer (security measure) which observes post area.
 */
function create_observer() {
    let observer;
  
    let options = {
      delay: 400,
      trackVisibility: true,
      threshold: 0.1,
    };
  
    observer = new IntersectionObserver(handle_intersect, options);
    observer.observe(document.getElementById("window"));
}

/**
 * Observer intersection handler. Called whenever something has changed in the observed area.
 * @param {*} entries Elements in observed area.
 * @param {*} observer Observer object.
 */
function handle_intersect(entries, observer) {
    for (const entry of entries) {
        console.log(entry.isVisible);
        console.log(entry);
        if (entry.isIntersecting && entry.isVisible) {
            console.log("Object is alright");
            block_actions = false;
        } else {
            console.log("Object is intersecting!");
            block_actions = true;
        }
    }
}
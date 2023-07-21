'use strict';
/** 
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @description  Configuration script.
*/

const ip = require('ip');
var config = {};

//config.host = '0.0.0.0';          // Hostname
config.host = 'localhost';
config.port = 80;                   // Server/client port
config.demo_port = 7287;            // Port for remote demonstration sites - Don't change this one
config.env = "development";       // development / production
//config.env = "production";

config.secret_key = "super secret key"; // Secret key for generating session ids

if (config.host === "localhost") config.host = ip.loopback("ipv4");
if (config.host === "0.0.0.0") config.host = ip.address();

console.log("Configuration:");
console.log("HOST: " + config.host);
console.log("PORT: " + config.port);
console.log("DEMO_PORT: " + config.demo_port);
console.log("ENV: " + config.env);

module.exports = config;
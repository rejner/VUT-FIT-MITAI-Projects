'use strict';
// WAP - Project 2 - Web vulnerabilities demonstration
/** 
* @name         main
* @author       Michal Rein (xreinm00@stud.fit.vutbr.cz)
* @version      Node - v16.14.0
* @description  Main script of the express project.
*/

const express = require('express');
const cors = require('cors');
const config = require('./config');

// Set live reaload for development purposes.
if (config.env === "development") {
    var livereload = require("livereload");
    var connectLiveReload = require("connect-livereload");
    const liveReloadServer = livereload.createServer();
    liveReloadServer.server.once("connection", () => {
        setTimeout(() => {
            liveReloadServer.refresh("/");
        }, 100);
    });
}

// **************************************
//      Remote demonstration sites
// ***************************************
const demos = express();
const demosPort = config.demo_port;
demos.use(express.static('demo_sites'));
demos.use(function(req, res, next) {
    res.status(404);
    res.send('Demo website not found :(');
});
demos.listen(demosPort, () => {
    console.log(`Demo sites are running on port ${demosPort}`);
});

// *********************************
//      Server backend setup
// *********************************
const server = express();
const serverPort = config.port;
const bodyParser = require('body-parser');

/* Setup API routes */
const chattingRouter = require('./server/routes/chatting.router');
const authRouter = require('./server/routes/auth.router');
const walletRouter = require('./server/routes/wallet.router');
const filesRouter = require('./server/routes/files.router');

/* Setup session */
var session = require('express-session')
var sess = {
    secret: config.secret_key,
    cookie: {},
    resave: false,
    saveUninitialized: true,
}
server.use(session(sess));                  // use session policy
server.use(express.static('./client'));     // serve client static files as frontend
server.use(bodyParser.json());              // use json parser
server.use('/chatting', chattingRouter);    // apply /chatting router
server.use('/auth', authRouter);            // apply /auth router
server.use('/files', filesRouter);          // apply /files router
server.use('/wallet', cors(                 // apply /wallet router with cors settings
    {
        origin: `http://${config.host}:${demosPort}`, // simulate Access-Control-Allow-Origin: *
        methods: ['GET', 'POST'],
        credentials: true,
        }), walletRouter);
        
// Default for unknown routes
server.use(function(req, res, next) {
    res.status(404);
    res.send('Server not found :(');
});

// Server listen
server.listen(serverPort, () => {
    console.log(`Server running on port ${serverPort}`)
});

// Connect live reload
if (config.env === "development") {
    server.use(connectLiveReload());    // DEBUG
}

# WAP - Project 2 - Web vulnerabilities demonstration application
<pre>
Author:     Michal Rein (xreinm00)
Email:      xreinm00@stud.fit.vutbr.cz
Date:       18.04.2022
</pre>

## Zadání

## Varianta: Vytvořte výukovou aplikaci demonstrující zranitelnosti XSS, clickjacking, CSRF a další

Vytvořte výukovou aplikaci spustitelnou na serveru eva (v rámci studentského webového prostoru) demonstrující zranitelnosti XSS, clickjacking, CSRF a dalších. V aplikaci implementujte i vhodné obrané techniky (např. bezpečnostní hlavičky HTTP).

#### Získáno bodů: 30/30

## Project structure

```
WAP-Project_2
│   README.md
│   jsdoc.conf              <--- JSDoc config
|   package.json
|   main.js                 <--- Server start script
│
└───client                  <--- frontend part
│   │   index.html          
│   │
│   └───css                 <--- css style sheets
│   |    │   ... ...
│   |       
|   └───pages               <--- HTML pages
│   |    │   ... ...
|   |      
│   └───scripts             <--- javascript files
│       │   ... ...
│   
└───server                  <--- backend part
|    │   
│    └───container          <--- filesystem simulation for demo
│    |    │   ... ...
│    |       
|    └───controllers        <--- API Endpoints controllers
│    |    │   ... ...
|    |      
│    └───routes             <--- API Endpoints routes definitions
│    |    │   ... ...
|    |      
│    └───services           <--- services for controllers
│       │   ... ...
|
└───demo_sites              <--- demo sites running out of same-origin
│   |
|   └───css                 <--- css style sheets
│   |    │   ... ...
│   |       
|   └───demos               <--- HTML demo pages
│   |    │   ... ...
|   |      
│   └───scripts             <--- javascript files
│       │   ... ...
|
└───docs                    <--- generated documentation
    │   index.html
    |   ... ...

```

## Used packages (npm)
 - ip - host ip address resolution
 - cors - cors policy settings
 - express - web server
 - express-session - express session management
 - jsdoc-route-plugin - jsdoc plugin for API routes annotation
 - nodemon  // dev
 - livereload   // dev
 - connect-livereload //dev

## Implementation
Project use express as web server, frontend is written in plain HTML/CSS/JS stack.

The main.js script will start the server on hostname and port specified by config.js file.
In addition, another instance of the server for serving remote demo static sites will
use port 7287. 

## Documentation
Generated by JSDoc:

    npx jsdoc -c jsdoc.conf

Output is generated into <i>docs</i> directory.

## How to run this project
Install required packages:

    npm install

Run project using any of these commands:

    npm start       <--- recommended 

    node main.js

    

    

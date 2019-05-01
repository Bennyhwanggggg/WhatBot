WhatBot -- the readme file
==========================

This file includes instruction on how tutor can run the system. 

Setup, build and run instruction

Prerequisites:
- Python 3.5 or above version installed. If you do not have this, install instruction here: https://www.python.org/downloads/
- npm 6 or above version installed. If you do not have this, install instruction here: https://www.npmjs.com/get-npm

Build and Run:
To run the whole system locally, a `Makefile` has being created. In this folder run:

```
Make
```

and you should see all the dependencies being installed.

After all the dependencies are installed, after about 30 seconds environment setup and loading, you'll be directed to the login screen of WhatBot and the app should be running on:

http://localhost:3000/login

And then you can test all the chatbot features with following account:

* Admin:

    * Username: z0000000, Password: 0000000

* Student: 

    * Username: z1234567, Password: 123456

    * Username: z8888888, Password: 123456

    * Username: z9999999, Password: 9999999


Alternatively, you can see the live deployed version on: https://whatbot9900.herokuapp.com/ 



Appendiex -- A: how to install `NodeJS` and `NPM`
=================================================

## Install npm

### npm is installed with Node.js

npm is distributed with [Node.js](https://nodejs.org/)- which means that when you download Node.js, you automatically get npm installed on your computer.

Download Node.js and npm

### Check that you have node and npm installed

To check if you have Node.js installed, run this command in your terminal:

```
node -v
```

To confirm that you have npm installed you can run this command in your terminal:

```
npm -v
```



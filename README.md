# WhatBot

Live version [here](https://whatbot9900.herokuapp.com/). **Note: As the project is now completed, we have taken down the backend database so AWS RDS won't start charging us.**  

WhatBot is a student-tutor support chatbot developed for Capstone Project of Master of IT at UNSW. This repository contains all the packages for the WhatBot software and it is managed as a mono-repo.  

## Setup, build and run

**Running locally**  
To run the whole system locally, a `Makefile` has being created. In this folder run:
```
Make
```
and you should see all the dependencies being installed and the whole app running afterwards.

Alternatively, you can see the deployed version which is live at [https://whatbot9900.herokuapp.com/](https://whatbot9900.herokuapp.com/). The deployed version is the most production ready
and stable one. To see how to do deployment or how it is done, please see the Deployment section below.

## Deployment

WhatBot can be found and used [https://whatbot9900.herokuapp.com/](https://whatbot9900.herokuapp.com/).  
It is deployed on Heroku using Docker. As a client-server architecture is used, the frontend and backend are each running in their own Docker container. In production build, both frontend and backend are running on their own nginx server inside their respective Docker container.

### How to deploy

#### Automatic deployment

Continuous integration and continous deployment using CircleCI has being setup to automatically deploy both frontend and backend to Heroku when changes to master branch is detected and the changes passes the tests.

#### Manual deployment

**Deploying to Heroku**  
To manually deploy to Heroku, you need to have Heroku CLI and Docker installed.  
[Install Heroku CLI here](https://devcenter.heroku.com/articles/heroku-cli).  
[Install Docker here](https://docs.docker.com/install/).  
After you have installed both of them:  
Log into Heroku CLI:
```
heroku login
```
Log into Heroku container registry:
```
heroku container:login
```
Deploy frontend
```
cd frontend
heroku container:push web -a whatbot9900
heroku container:release web -a whatbot9900
```
Deploy backend
```
cd backend
heroku container:push web -a whatbot9900backend
heroku container:release web -a whatbot9900backend
```
More information on Heroku container registry [here](https://devcenter.heroku.com/articles/container-registry-and-runtime)

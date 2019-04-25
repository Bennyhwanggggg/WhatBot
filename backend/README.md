# WhatBot Backend

This packages contains the backend modules of WhatBot. It is a Python Flask app and the main app code is located at `app.py`. In production mode, uWSGI and nginx web server are used for to run the Flask app in a more stable and optimize performance.
In deployment, production mode is used and the *Docker* is used to run the backend application. However, the `Dockerfile`, *nginx* and *uwsgi* webservers are only configured to work when running on a HTTPS server like Heroku and will not work for running locally.
 Therefore, we have only provided instruction on how to run locally here. gi 

## Setup, build and run

**Running locally**  
*Prerequisites*: Python 3 installed  
Setup
```
python3 -m pip install -r requirements.txt
python3 setup.py install
```
Run
```
python3 app.py
```

## Testing

Pytest is the chosen testing module for our backend. All test cases are inside the `tests` folder. The test covers 
most of the backend module's essential functions.  

### How to test?

First ensure that pytest is installed. If not use:
```
pip install pytest
```
To test you can use either the call script that has being set up in this root folder
```
./start_test.sh
```
or call pytest in the command line in this root folder
```
pytest
```
To specify a specific test case:
```
pytest -k {test case name}
```

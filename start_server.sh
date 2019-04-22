#!/bin/sh

# setup dependencies for frontend
(cd frontend || exit; npm install) & 
# setup dependencies for backend then launch
(cd backend || exit; python3 -m pip install virtualenv --user; python3 -m virtualenv venv; source venv/bin/activate; python3 -m pip install -r requirements.txt; python3 setup.py install; python3 app.py) 

cd frontend
npm start
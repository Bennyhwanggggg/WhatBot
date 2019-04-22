#!/bin/sh

# setup dependencies
cd backend
python3 -m pip install virtualenv --user
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 setup.py install
deactivate
cd ../frontend
npm install
cd ..

 # run backend then frontend	
(cd backend || exit; source venv/bin/activate; python3 app.py) &
cd frontend || exit; npm start

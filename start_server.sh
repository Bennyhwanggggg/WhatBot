#!/bin/sh

# setup dependencies for backend
(cd backend || exit; python3 -m pip install virtualenv --user; python3 -m virtualenv venv; source venv/bin/activate; python3 -m pip install -r requirements.txt; python3 setup.py install) &
# setup dependencies for frontend
(cd frontend || exit; npm install)

cd ..

# run backend then frontend
(cd backend || exit; python3 app.py) &
cd frontend || exit; npm start


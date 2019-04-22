#!/bin/sh


(cd backend || exit; python3 app.py) &

cd frontend || exit; npm start


#!/usr/bin/python
import psycopg2
from flask import (Flask, request, abort, jsonify)

app = Flask(__name__)


@app.route('/lecturer', methods = ["get"])
def connect_lecturer():
    try:
        connection = psycopg2.connect(user = "",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "user")
        cursor = connection.cursor()
        print ( connection.get_dsn_parameters(),"\n")

        cursor.execute("SELECT * from lecturer")
        result=cursor.fetchall()
        print("result of lecturer: ", result,'\n')
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return jsonify(result)


@app.route('/timeslot/<int:tid>', methods = ["POST"])
def set_time_avail(tid):
    try:
        connection = psycopg2.connect(user = "",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "user")
        cursor = connection.cursor()
        print(tid)
        cursor.execute("UPDATE Timeslot SET available = %s  WHERE tid = %s",(False,tid))
        cursor_1 = connection.cursor()
        cursor_1.execute("SELECT tid, start_time, end_time, available from Timeslot Where tid = %s",(tid,))
        result =str(cursor_1.fetchall())
        connection.commit()
        
        print("timeslot: ", result,'\n')
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return jsonify(result)

 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
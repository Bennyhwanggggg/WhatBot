#!/usr/bin/python
import psycopg2

# select the data from lecturer table
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
    return result

#set time slot as booked by tid
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
    return result

#add data into course list table
def add_handbook_course_list(Course_code, Course_name, Timetable, ADK, Comment):
    try:
        connection = psycopg2.connect(user = "",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "handbook")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO course_list(Course_code, Course_name, Timetable, ADK, Comment) VALUES (%s,%s,%s,%s,%s)",(Course_code, Course_name, Timetable, ADK, Comment))
       
        connection.commit()
        print("add data into course_list successfully!!")
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return None

#get the data from course_list
def connect_course_list(cid):
    try:
        connection = psycopg2.connect(user = "",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "handbook")
        cursor = connection.cursor()
        print ( connection.get_dsn_parameters(),"\n")

#         cursor.execute("SELECT * from course_list")
        cursor.execute("SELECT * from course_list where course_code like %s", ("%"+cid,))
        result=cursor.fetchall()
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return result

 
if __name__ == '__main__':
    result = connect_course_list(cid)
    print("data in course list: ", result)
#     app.run(debug=True, host='0.0.0.0')

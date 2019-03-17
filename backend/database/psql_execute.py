import psycopg2

def get_data(query):
    try:
        connection = psycopg2.connect(
            database="Master9900",
            user="master9900",
            password="12345678",
            host="master9900.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
            port='5432'
        )
        cursor = connection.cursor()
        print("query:", query)
        cursor.execute(query)
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

def get_course_outline(cid):
    key_part = '%' + cid
    # "SELECT * from course_list where course_code like '%COMP9900'"
    query = "SELECT description,outline_url from info_handbook where CID like '%s'"%key_part
    print("query: ", query)
    return get_data(query)

# select the data from lecturer table
def connect_lecturer():
    try:
        connection = psycopg2.connect(user = "Master9900",
                                    password = "12345678",
                                    host = "master9900.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                    port = "5432",
                                    database = "Master9900")
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
        connection = psycopg2.connect(user = "Master9900",
                                    password = "12345678",
                                    host = "master9900.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                    port = "5432",
                                    database = "Master9900")
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
def add_courselist(course_code, course_name, timetable, ADK, comment):
    try:
        connection = psycopg2.connect(user = "Master9900",
                                  password = "12345678",
                                  host = "master9900.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                  port = "5432",
                                  database = "Master9900")
        print("23434")
        print(connection)
        print("lllaaaa")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO courselist(course_code, course_name, timetable, ADK, comment) VALUES (%s,%s,%s,%s,%s)",(course_code, course_name, timetable, ADK, comment))

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


#add data into course list table
def add_handbook(CID, title, credit, prerequisite, outline_url, faculty_url, school_url, Offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, international_std):
    try:
        connection = psycopg2.connect(user = "",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "handbook")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO info_handbook(CID, title, credit, prerequisite, outline_url, faculty_url, school_url, Offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, international_std) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(CID, title, credit, prerequisite, outline_url, faculty_url, school_url, Offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, international_std))

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
        connection = psycopg2.connect(user = "Master9900",
                                    password = "12345678",
                                    host = "master9900.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                    port = "5432",
                                    database = "Master9900")
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
    #add_courselist("COMP9321", "Software Service Design and Engineering", "http://timetable.unsw.edu.au/2019/COMP9322.html", "X", "hello")
    result = connect_course_list(cid)
    print("data in course list: ", result)
#     app.run(debug=True, host='0.0.0.0')

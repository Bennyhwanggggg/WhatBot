#!/usr/bin/python
import psycopg2

def get_data(query):
    try:
        connection = psycopg2.connect(
            user = "whatbot",
            password = "12345678",
            host = "whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
            port = "5432",
            database = "postgres"
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
        connection = psycopg2.connect(user = "whatbot",
                                    password = "12345678",
                                    host = "whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                    port = "5432",
                                    database = "postgres")
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
        connection = psycopg2.connect(user = "whatbot",
                                    password = "12345678",
                                    host = "whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                    port = "5432",
                                    database = "postgres")
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
        connection = psycopg2.connect(user = "whatbot",
                                  password = "12345678",
                                  host = "whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                  port = "5432",
                                  database = "postgres")
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
        connection = psycopg2.connect(user = "whatbot",
                                  password = "12345678",
                                  host = "whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                  port = "5432",
                                  database = "postgres")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO info_handbook(cid, title, credit, prerequisite, outline_url, faculty_url, school_url, Offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, international_std) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(CID, title, credit, prerequisite, outline_url, faculty_url, school_url, Offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, international_std))

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
        connection = psycopg2.connect(user = "whatbot",
                                    password = "12345678",
                                    host = "whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com",
                                    port = "5432",
                                    database = "postgres")
        cursor = connection.cursor()
        print ( connection.get_dsn_parameters(),"\n")

#         cursor.execute("SELECT * from course_list")
        cursor.execute("SELECT * from courselist where course_code like %s", ("%"+cid,))
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
    #add_courselist("COMP9222", "Digital Circuits and Systems", "http://timetable.unsw.edu.au/2019/COMP9222.html", "", "")
    # add_handbook("COMP3900",
    #             "Handbook 2019 - Course - Computer Science Project - COMP3900",
    #             "6 Units of Credit",
    #             "Prerequisite: COMP1531, and COMP2521 or COMP1927, and enrolled in a BSc Computer Science major with completion of 120 uoc",
    #             "https://www.engineering.unsw.edu.au/computer-science-engineering",
    #             "http://www.eng.unsw.edu.au",
    #             "http://www.cse.unsw.edu.au/",
    #             "Term 1, Term 2, Term 3",
    #             "Kensington",
    #             "A capstone software project. Students work in teams to define, implement and evaluate a real-world software system. Most of the work in this course is team-based project work, although there are some introductory lectures on software project management and teamwork strategies. Project teams meet fortnightly with project mentors to report on the progress of the project. Assessment is based on a project proposal, a final project demonstration and report, and on the quality of the software system itself. Students are also required to reflect on their work and to provide peer assessment of their team-mates' contributions to the project.",
    #             "https://itq9q5ny14.execute-api.ap-southeast-2.amazonaws.com/prod/pdf?url=https://www.handbook.unsw.edu.au/undergraduate/courses/2019/COMP3900/",
    #             "10",
    #             "$1170",
    #             "$5790",
    #             "$5790")
    # a = connect_course_list("COMP9321")
    # print(a)
    result = connect_course_list(cid)
    #print("data in course list: ", result)
    app.run(debug=True, host='0.0.0.0')

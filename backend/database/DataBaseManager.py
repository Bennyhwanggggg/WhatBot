import psycopg2

HOST = 'whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com'
USERNAME = 'whatbot'
PASSWORD='12345678'
DATABASE = "postgres"
PORT = '5432'


class DataBaseManager:
    def __init__(self, host=HOST, port=PORT, database_name=DATABASE):
        self.host, self.port, self.database_name = host, port, database_name
        self.connection, self.cursor = None, None

    def connect(self):
        self.connection = psycopg2.connect(database=self.database_name,
                                           user=USERNAME,
                                           password=PASSWORD,
                                           host=self.host,
                                           port=str(self.port))
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()
        print('Connection to AWS opened')

    def disconnect(self):
        if self.connection and self.cursor:
            self.cursor.close()
            self.connection.close()
            print('Connection to AWS closed')
        self.connection, self.cursor = None, None

    def execute_query(self, query):
        result = None
        try:
            if not self.connection and not self.cursor:
                self.connect()
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except (Exception, psycopg2.Error) as e:
            print("Error executing query:\n{}".format(str(e)))
        finally:
            self.disconnect()
        print('Query is: {}\nResult is: {}'.format(query, result))
        return result

    #def get_course_outline(self, cid):
        #query = "SELECT description,outline_url from info_handbook where cid like '{}'".format('%{}'.format(cid))
        #return self.execute_query(query)

    def get_course_outline(self, cid):
        key_part = '%' + cid
        query = "SELECT description,outline_url from info_handbook where cid like '%s'"%key_part
        result_arr = self.execute_query(query)
        return result_arr[0][0] + "for more information go to " + result_arr[0][1]

    def get_all_lecturers(self):
        query = "SELECT * from lecturer"
        return self.execute_query(query)

    def make_consultation_booking(self, tid):
        query = "UPDATE Timeslot SET available = {}  WHERE tid = {}".format('False', tid)
        return self.execute_query(query)

    def get_consultation_timeslots(self, tid):
        query = "SELECT tid, start_time, end_time, available from Timeslot Where tid = {}".format(tid)
        return self.execute_query(query)

    def add_course(self, course_code, course_name, timetable, ADK, comment):
        query = "INSERT INTO courselist(course_code, course_name, timetable, ADK, comment) VALUES ({},{},{},{},{})".format(
        course_code, course_name, timetable, ADK, comment)
        return self.execute_query(query)

    def add_handbook_entry(self, cid, title, credit, prerequisite, outline_url, faculty_url, school_url, offer_term,
                           campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std,
                           international_std):
        query = "INSERT INTO info_handbook(cid, title, credit, prerequisite, outline_url, faculty_url, school_url, " \
        "Offer_term, campus, description, pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, " \
        "international_std) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
        cid, title, credit, prerequisite, outline_url, faculty_url, school_url, offer_term, campus, description,
        pdf_url, indicative_contact_hr, commonwealth_std, domestic_std, international_std)
        return self.execute_query(query)

    def get_course(self, cid):
        query = "SELECT * from course_list where course_code like {}".format('%{}'.format(cid))
        return self.execute_query(query)


if __name__ == '__main__':
    data_base_manager = DataBaseManager()
    result = data_base_manager.get_course_outline("COMP3900")
    print("outline: ", result)



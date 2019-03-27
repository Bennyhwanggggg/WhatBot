import psycopg2
import re

HOST = 'whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com'
USERNAME = 'whatbot'
PASSWORD='12345678'
DATABASE = "postgres"
PORT = '5432'


class Consultation:
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

    def execute_query(self, query, *args):
        result = None
        try:
            if not self.connection and not self.cursor:
                self.connect()
            if args:
                self.cursor.execute(query, (args[0]))
            else:
                self.cursor.execute(query)
            regex = re.compile(r'SELECT', re.IGNORECASE)
            result = self.cursor.fetchall() if regex.search(query) else "execute successfully"
        except (Exception, psycopg2.Error) as e:
            print("Error executing query:\n{}".format(str(e)))
        finally:
            self.disconnect()
        print('Query is: {}\nResult is: {}'.format(query, result))
        return result

    def add_consultation(self, cid, sid, time, date):
        query = "INSERT INTO consultation(cid, sid, time, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, sid, time, date)
        return self.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time):
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s"
        inputs = (cid, sid, time)
        return self.execute_query(query, inputs)

    def check_avail_timeslot(self, cid):
        initial_timeslots = ['9:00AM','10:00AM', '11:00AM', '12:00AM', '1:00PM', '2:00PM', '3:00PM', '4:00PM', '5:00PM']
        key_part = '%' + cid
        query = "SELECT time from consultation where cid like %s"
        inputs = (key_part, )
        booked = list(self.execute_query(query, inputs)[0])
        print("booked", booked)
        avail_timeslot = []
        for time in initial_timeslots:
            if time not in booked:
                print(time)
                avail_timeslot.append(time)
        return avail_timeslot


if __name__ == "__main__":
    consultation = Consultation()
    #array = consultation.add_consultation("COMP9900", "z123456", "9:00AM", '{2013-06-01}')
    #array = consultation.delete_consultation("COMP9900", "z123456", "9:00AM")
    array = consultation.check_avail_timeslot("COMP9900")
    print(array)



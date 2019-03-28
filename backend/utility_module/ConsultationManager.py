from database.DataBaseManager import DataBaseManager
import datetime


class ConsultationManager:
    def __init__(self):
        self.data_base_manager = DataBaseManager()

    def add_consultation(self, cid, sid, time, date):
        query = "INSERT INTO consultation(cid, sid, time, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, sid, time, date)
        return self.data_base_manager.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time):
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s"
        inputs = (cid, sid, time)
        return self.data_base_manager.execute_query(query, inputs)

    def check_avail_timeslot(self, cid):
        initial_timeslots = ['9:00AM','10:00AM', '11:00AM', '12:00AM', '1:00PM', '2:00PM', '3:00PM', '4:00PM', '5:00PM']
        key_part = '%' + cid
        query = "SELECT time from consultation where cid like %s"
        inputs = (key_part, )
        booked = list(self.data_base_manager.execute_query(query, inputs)[0])
        print("booked", booked)
        avail_timeslot = []
        for time in initial_timeslots:
            if time not in booked:
                print(time)
                avail_timeslot.append(time)
        return avail_timeslot
    
    def update_consultation(self):#update the consultation database everyday
        date = datetime.datetime.today().strftime('%Y-%m-%d')#eg. 2019-03-28
        key_part = '%' + date
        query = "DELETE FROM consultation WHERE date < %s"
        inputs = (key_part, )
        return self.execute_query(query, inputs)


if __name__ == "__main__":
    consultation = Consultation()
    #array = consultation.add_consultation("COMP9900", "z123456", "9:00AM", '{2013-06-01}')
    #array = consultation.delete_consultation("COMP9900", "z123456", "9:00AM")
    array = consultation.check_avail_timeslot("COMP9900")
    print(array)

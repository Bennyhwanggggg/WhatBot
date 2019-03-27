from consultation.DataBaseManager import Consultation
if __name__ == "__main__":
    consultation = Consultation()
    array = consultation.add_consultation("COMP9900", "z123456", "9:00AM", '{2013-06-01}')
    array = consultation.check_avail_timeslot("COMP9900")
    array = consultation.delete_consultation("COMP9900", "z123456", "9:00AM")

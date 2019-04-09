"""
    This is a mock database class used for tests only. It copies the functionality
    of a relational database
"""
import pandas as pd


class MockDatabase:
    def __init__(self, type, column_names=[]):
        self.type = type
        self.columns = column_names
        self.database = pd.DataFrame(columns=self.columns)

    def setup_mock_consultation_data(self, course_codes, zids, times, dates):
        if self.type != 'CONSULTATION':
            return
        idx = 0
        for course_code, zid, time, date in zip(course_codes, zids, times, dates):
            self.database.loc[idx] = [course_code, zid, time, date]
            idx += 1

    def add_consultation(self, cid, sid, time, date):
        if self.type != 'CONSULTATION':
            return
        self.database.loc[-1] = [cid, sid, time, date]
        return ''

    def get_time_slots(self, cid, date):
        if self.type != 'CONSULTATION':
            return
        time_table = self.database[(self.database['cid'] == cid) & (self.database['date'] == date)]
        return time_table['time'].tolist()

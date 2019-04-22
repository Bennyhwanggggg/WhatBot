"""
    This is a mock emailer class that is used for testing only
    It copies the functionality of Utility Module's emailer.
"""


class MockEmailer:
    def send_outline(self, subject, msg, cid, receiver):
        print('Send outline:\nSubject: {}\n msg: {}\n cid:{}\n receiver:{}'.format(subject, msg, cid, receiver))

    def send_confirm_booking(self, cid, receiver, date, time):
        print('Send confirmation booking:\ncid: {}\n receiver: {}\n date:{}\n time:{}'.format(cid, receiver, date, time))

    def send_confirm_cancelling(self, cid, receiver, date, time):
        print('Send cancel booking:\ncid: {}\n receiver: {}\n date:{}\n time:{}'.format(cid, receiver, date, time))
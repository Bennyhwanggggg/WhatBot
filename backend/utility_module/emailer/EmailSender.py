"""
    The EmailSender class is responsible for email related operations such
    as sending course outline pdf files, confirmation emails for booking
    consultation and cancelling a booking consultation.
"""
import smtplib
from utility_module.emailer.config import EMAIl_ADDRESS, PASSWORD
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log


class EmailSender:
    def __init__(self, email_address=EMAIl_ADDRESS, password=PASSWORD):
        """Instantiate the class with an email account

        :param email_address: email account
        :type: str
        :param password: password of that email account
        :type: str
        """
        self.email_address = email_address
        self.password = password

    def send_outline(self, subject, msg, cid, receiver):
        """Send course outline's pdf file to receiver. The body of email is already prefixed.

        :param subject: Subject of the email
        :type: str
        :param msg: message in the body
        :type: str
        :param cid: course id of the course
        :type: str
        :param receiver: reciever's email address
        :type: str
        :return: None
        """
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(self.email_address, self.password)
            message = MIMEMultipart("alternative")
            message["Subject"] = "{} of {}".format(subject, cid)

            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   This is course outline of {}:<br>
                   <h3><a href={}>Course Outline</a><h3>
                </p>
              </body>
            </html>
            """.format(cid, msg)

            part1 = MIMEText(html, "html")
            message.attach(part1)

            server.sendmail(self.email_address, receiver, message.as_string())
            server.quit()
            logger.info("Success: Email sent to {}!".format(receiver))
        except Exception as e:
            logger.error(str(e))

    def send_confirm_booking(self, cid, receiver, date, time):
        """Send consultation booking confirmation email using the set email body below.

        :param cid: course id of the booking
        :type: str
        :param receiver: receiver email
        :type: str
        :param date: date of the booking
        :type: str
        :param time: time of the booking
        :type: str
        :return: None
        """
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(self.email_address, self.password)
            message = MIMEMultipart("alternative")
            message["Subject"] = "Booking confirmation"

            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   You have successfully booked a consultation for {} at {} on {}
                </p>
              </body>
            </html>
            """.format(time, date, cid)

            part1 = MIMEText(html, "html")
            message.attach(part1)

            server.sendmail(self.email_address, receiver, message.as_string())
            server.quit()
            logger.info("Success: Email sent to {}!".format(receiver))
        except Exception as e:
            logger.error(str(e))

    def send_confirm_cancelling(self, cid, receiver, date, time):
        """Send consultation booking confirmation email using the set email body below.

        :param cid: course id of the booking
        :type: str
        :param receiver: receiver email
        :type: str
        :param date: date of the booking
        :type: str
        :param time: time of the booking
        :type: str
        :return: None
        """
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(self.email_address, self.password)
            message = MIMEMultipart("alternative")
            message["Subject"] = "Cancelling confirmation"

            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   You have successfully cancelled your consultation booking for {} at {} on {}
                </p>
              </body>
            </html>
            """.format(time, date, cid)

            part1 = MIMEText(html, "html")
            message.attach(part1)

            server.sendmail(self.email_address, receiver, message.as_string())
            server.quit()
            logger.info("Success: Email sent to {}!".format(receiver))
        except Exception as e:
            logger.error(str(e))

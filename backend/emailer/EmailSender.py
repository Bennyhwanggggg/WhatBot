import smtplib
from emailer.config import EMAIl_ADDRESS, PASSWORD
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log


class EmailSender:
    def __init__(self, email_address=EMAIl_ADDRESS, password=PASSWORD):
        self.email_address = email_address
        self.password = password

    def send_outline(self, subject, msg, cid, receiver):
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
                   This is outline of {}:<br>
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

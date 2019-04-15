import smtplib
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class sending:
    def __init__(self, subject, msg, cid):
        self.subject = subject
        self.msg = msg
        self.cid = cid

    def outline(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIl_ADDRESS, config.PASSWORD)
            message = MIMEMultipart("alternative")
            message["Subject"] = "{} of {}".format(self.subject, self.cid)

            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   This is outline of {}:<br>
                   <h3><a href={}>Course Outline</a><h3>
                </p>
              </body>
            </html>
            """.format(self.cid, self.msg)

            part1 = MIMEText(html, "html")
            message.attach(part1)

            server.sendmail(config.EMAIl_ADDRESS, config.EMAIl_ADDRESS, message.as_string())
            server.quit()
            print("Success: Email sent!")
            return "Success: Email sent(:"
        except:
            print("Email failed to send")
            return "Email failed to send:("



if __name__ == '__main__':
     subject = "Outline"
     msg = "https://www.engineering.unsw.edu.au/computer-science-engineering"
     cid = 'COMP9900'
     email = sending(subject, msg, cid)
     email.outline()



import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders


SUBJECT = "Email Data"

msg = MIMEMultipart()
msg['Subject'] = SUBJECT 
msg['geoffreywestgis@gmail.com'] = self.EMAIL_FROM
msg['geoffreywestgis@gmail.com'] = ', '.join(self.EMAIL_TO)

part = MIMEBase('application', "octet-stream")
part.set_payload(open("C:\Users\GIS\Desktop\soap_geodatabase.py", "rb").read())
Encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="C:\Users\GIS\Desktop\soap_geodatabase.py"')

msg.attach(part)

server = smtplib.SMTP(smtp.gmail.com)
server.sendmail("geoffreywestgis@gmail.com", "geoffreywestgis@gmail.com, msg.as_string())
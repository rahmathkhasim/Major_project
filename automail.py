import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE

# Define sender and receiver email addresses
sender = 'vararaghuram003@gmail.com'
password = 'your_password_here'  # Replace with your actual password
receivers = ['vararaghuram002@gmail.com']

# Define email message
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = COMMASPACE.join(receivers)
msg['Subject'] = 'Attendance'

# Add CSV file attachment
filename = 'StudentDetails/StudentDetails.csv'  # Use forward slashes
try:
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={filename}")
    msg.attach(part)
except FileNotFoundError:
    print("File not found. Please check the file path.")
    exit()

# Send email using SMTP server
try:
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(sender, password)
    smtpserver.sendmail(sender, receivers, msg.as_string())
    smtpserver.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")

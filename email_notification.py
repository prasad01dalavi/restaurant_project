import smtplib


sender = ""     # sender email id
password = ""   # sender password


def send(receiver, subject, text):
    session = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session
    session.starttls()  # start TLS for security
    session.login(sender, password)  # Authentication
    message = f'Subject: {subject}\n\n{text}'
    session.sendmail(sender, receiver, message)
    session.quit()  # terminating the session
    print(f'[INFO] Email Sent!')

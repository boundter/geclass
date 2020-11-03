import smtplib
from email.message import EmailMessage


def SendEmail(recipient, subject, content):
    server_ip = "172.17.0.1"  # ip of the smtp server
    sender_mail = "no-reply@geclass.physik.uni-potsdam.de"
    content += "\n\n-----------------------\n"
    content += "Bitte antworten Sie nicht auf diese Email, nutzen Sie stattdessen ge-class@uni-potsdam.de"
    message = EmailMessage()
    message.set_content(content)
    message["Subject"] = subject
    message["From"] = "GE-CLASS <no-reply@geclass.physik.uni-potsdam.de>"
    message["To"] = recipient
    with smtplib.SMTP(server_ip) as server:
        server.send_message(message)

import smtplib

def SendMail(recipient, subject, content):
    server_ip = "172.17.0.1"  # ip of the smtp server
    sender_mail = "no-reply@geclass.physik.uni-potsdam.de"
    message = """
    To: {}
    From: GEClass <{}>
    Subject: {}
    MIME-Version: 1.0
    Content-Type: text/plain; charset=utf-8
    Content-Transfer-Encoding: 8bit

    {}
    --------------------------------
    Bitte antworten Sie nicht auf diese EMail.
    Zur Kontaktaufnahme nutzen Sie bitte ge-class@uni-potsdam.de
    """.format(recipient, sender_mail, subject, content)
    with smtplib.SMTP(server_ip) as server:
        server.sendmail(sender_mail, recipient, content)




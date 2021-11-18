import smtplib
from email.mime.text import MIMEText
from email.header import Header

class SmtpClient():
    def __init__(self,server_url,port=465,use_ssl=True):
        if use_ssl:
            self.server = smtplib.SMTP_SSL(server_url,port)
        else:
            self.server = smtplib.SMTP(server_url,port)

    def login(self,username,password):
        self.email = username
        self.server.login(username,password)
        return self

    def __enter__(self):
        return self

    def __exit__(self,type, value, trace):
        self.server.close()
    
    def sendText(self,to,subject,contain):
        try:
            msg = MIMEText(contain,'plain','utf-8')
            msg["From"] = self.email
            msg["To"] = ','.join(to) if isinstance(to,list) else to
            msg["Subject"] = Header(subject,'utf-8').encode()
            self.server.sendmail(self.email,to,msg.as_string())
            return True
        except:
            return False

    def close(self):
        self.server.close()

if __name__=="__main__":
    pass


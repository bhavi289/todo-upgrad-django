import requests
from .models import *

from datetime import datetime, timedelta
from django.db.models import Q

def send_email(user, pwd, recipient, title):
    import smtplib
    from email.mime.application import MIMEApplication
    from os.path import basename
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import sys, traceback
    from email.utils import COMMASPACE, formatdate
    # from email.MIMEBase import MIMEBase
    # from email import Encoders
    try:
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = recipient
        msg['Subject'] = "Reminder for " + title
        message = "Hello from Schedule It! This is a reminder for your task which is in 10 mins."
        msg.attach(MIMEText(message))
        
        mailserver = smtplib.SMTP('smtp.gmail.com',587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(user, pwd)
        
        mailserver.sendmail(user,recipient,msg.as_string())
        
        mailserver.quit()
    except Exception as e:
        print (e)
        send_email(user, pwd, recipient, title)

def reminder_mail(recipient, title):
   return send_email('csb.iiits@gmail.com', 'csb@iiits', recipient, title )

def check_reminder():
    print ("checking")
    now = datetime.now()

    date_now = datetime.now().date()
    time_now = datetime.now().time()

    now_plus_10 = now + timedelta(minutes = 10)
    time_plus_10 = now_plus_10.time()

    print (now, now_plus_10)

    all_tasks = Schedule.objects.filter(Q(date__gte = date_now) & Q (time__gte = time_now ) & Q (time__lte = time_plus_10 ) & Q(notified=False))
    print (all_tasks.count())
    for task in all_tasks:
        
        reminder_mail(task.user.email, task.title)
        task.notified = True
        task.save()
    '''
    return HttpResponse("done")
    '''
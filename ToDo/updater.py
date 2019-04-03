from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Schedule import send_reminder

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminder.check_reminder, 'interval', minutes=1)
    scheduler.start()
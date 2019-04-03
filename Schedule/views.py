from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required

from .models import Schedule
# Create your views here.

@login_required
def Home(request):
    if request.method == "GET":
        save = None
        now = datetime.now()

        date_now = datetime.now().date()
        time_now = datetime.now().time()
        
        if request.GET.get('save'):
            save = int(request.GET.get('save'))

        tasks = Schedule.objects.filter(user=request.user, completed=False)
        # tasks = Schedule.objects.filter(Q(user=request.user) & Q(Q(date__gt = date_now) | Q(date=date_now, time__gte = time_now)))
        return render(request, 'Schedule/home.html', {"tasks":tasks, "save":save})


'''
    Function being used for all CRUD functionalities
'''
@login_required
def AddSchedule(request):
    if request.method == "POST":
        try:
            if "taskAdd" in request.POST:
                title = request.POST.get('name')
                content = request.POST.get('description')
                date = request.POST.get('date')
                time = request.POST.get('time')
                if title=="" or content=="" or date=="" or time=="":
                    return HttpResponseRedirect(reverse("Schedule:Home")+"?save=0")
                # dt = datetime.datetime.strptime(date+"  "+time, "%Y/%m/%d %H:%M")
                s = Schedule()
                s.title = title
                s.date = date
                s.time = time
                s.content = content
                s.user = request.user
                # s.task_on.date = dt
                s.save()
                return HttpResponseRedirect(reverse("Schedule:Home")+"?save=1")
                # return HttpResponse("done")

            elif "taskDelete" in request.POST:
                checkedlist = request.POST.getlist("checkedbox")
                print (checkedlist)
                for task_id in checkedlist:
                    s = Schedule.objects.get(id=int(task_id))
                    s.delete()
                return HttpResponseRedirect(reverse("Schedule:Home")+"?save=2")
            
            elif "taskEdit" in request.POST:
                try:
                    s_id = request.POST.get('id_edit')
                    title = request.POST.get('name_edit')
                    content = request.POST.get('description_edit')
                    date = request.POST.get('date_edit')
                    time = request.POST.get('time_edit')
                    if title=="" or content=="" or date=="" or time=="":
                        return HttpResponseRedirect(reverse("Schedule:Home")+"?save=0")
                    print (s_id, title, content, date, time)
                    s = get_object_or_404(Schedule, id=int(s_id))
                    print (s)
                    s.title = title
                    s.date = date
                    s.time = time
                    s.content = content
                    # s.user = request.user
                    s.save()
                    return HttpResponseRedirect(reverse("Schedule:Home")+"?save=3")
                except Exception as e:
                    print (e)
                    pass
            
            elif "taskComplete" in request.POST:
                checkedlist = request.POST.getlist("checkedbox")
                print (checkedlist)
                for task_id in checkedlist:
                    tasks = Schedule.objects.filter(id=int(task_id))
                    for task in tasks:
                        task.completed = True
                        task.save()
                return HttpResponseRedirect(reverse("Schedule:Home")+"?save=4")

                # return HttpResponse("deleted")
        except Exception as e:
            print (e)
            return HttpResponseRedirect(reverse("Schedule:Home")+"?save=0")

@login_required
def AllTasks(request):
    if request.method == "GET":
        # remain = Schedule.objects.filter(Q(user=request.user) & Q(Q(date__gt = date_now) | Q(date=date_now, time__gte = time_now)))
        completed_tasks = Schedule.objects.filter(completed=True, user=request.user)
        remaining_tasks = Schedule.objects.filter(completed=False, user=request.user)
        return render(request, 'Schedule/all-tasks.html', {'completed_tasks':completed_tasks, 'remaining_tasks':remaining_tasks})


''' 
    Not Using these Functions Here
'''
@login_required
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

@login_required
def reminder_mail(recipient, title):
   return send_email('csb.iiits@gmail.com', 'csb@iiits', recipient, title )

@login_required
def check_reminder(request):
    now = datetime.now()

    date_now = datetime.now().date()
    time_now = datetime.now().time()

    now_plus_10 = now + timedelta(minutes = 10)
    time_plus_10 = now_plus_10.time()

    print (now, now_plus_10)

    all_tasks = Schedule.objects.filter(Q(date__gte = date_now) & Q (time__gte = time_now ) & Q (time__lte = time_plus_10 ) & Q(notified=False))
    print (all_tasks)
    for task in all_tasks:
        
        reminder_mail(task.user.email, task.title)
        task.notified = True
        task.save()

    return HttpResponse("done")

# def EditSchedule(request):
#     if request.method == 
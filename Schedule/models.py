from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True, null=True)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # due date
    time = models.TimeField(null=True, blank=True) # due time
    notified = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    task_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id) + " " + self.user.username + " " + str(self.date) + " - " + str(self.time)
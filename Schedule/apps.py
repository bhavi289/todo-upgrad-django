from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = 'Schedule'

    def ready(self):
        from ToDo import updater
        updater.start()

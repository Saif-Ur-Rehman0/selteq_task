import time
from django.core.management.base import BaseCommand
from TaskApp.models import Task

class Command(BaseCommand):
    help = 'Prints all tasks in the database one by one every 10 seconds'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all() 

        for task in tasks:
            self.stdout.write('Task Title: ' + str(task.title)) 
            self.stdout.write('Task Duration: ' + str(task.duration))
            time.sleep(10)
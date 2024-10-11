from celery import shared_task
import time

@shared_task
def print_tasks():
    from TaskApp.models import Task

    tasks = Task.objects.filter(user_id=1)
    for task in tasks:
        print(f"Task Title: {task.title}, Duration: {task.duration}, Timestamp: {task.created_at}")
        time.sleep(60)

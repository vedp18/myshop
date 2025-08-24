import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')
# By defninig the namespace, we will need to use CELERY_ prefix for all celery-related settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all installed Django apps.
# Celery will look for tasks.py in each app.
app.autodiscover_tasks()
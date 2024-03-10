#импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery
import os
from celery import Celery

#cвязываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации.
app = Celery('project')
#указываем пространство имен, чтобы Celery сам находил все необходимые настройки
#в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***».
app.config_from_object('django.conf:settings', namespace='CELERY')
# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
app.autodiscover_tasks()

from django.apps import AppConfig
from django.db import connection

class ApimapConfig(AppConfig):
    name = 'apimap'


def my_custom_sql(self):
    with connection.cursor() as cursor:
        data = cursor.execute("SELECT * FROM water")
        

    return data

data = my_custom_sql(self)
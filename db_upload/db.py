import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.chdir("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_test.settings")
django.setup()

from api.models import Category

Category.objects.create(name='GET')
Category.objects.create(name='POST')
Category.objects.create(name='PUT')
Category.objects.create(name='DELETE')



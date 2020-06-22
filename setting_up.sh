#!/bin/sh
python manage.py migrate

python db_upload/db.py

ipconfig getifaddr en0

python manage.py runserver 0:8000


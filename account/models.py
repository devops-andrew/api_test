from django.db import models

class Account(models.Model):
    name       = models.CharField(max_length = 50)
    email      = models.CharField(max_length = 200)
    password   = models.CharField(max_length = 500)
    profile    = models.ForeignKey('Profile', on_delete = models.SET_NULL, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'accounts'

class Profile(models.Model):
    hobby   = models.CharField(max_length = 300, null = True)
    address = models.CharField(max_length = 500, null = True)
    code    = models.CharField(max_length = 400, null = True)

    class Meta:
        db_table = 'profiles'


from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'categories'

class Mission(models.Model):
    name        = models.CharField(max_length = 50)
    description = models.CharField(max_length = 3000)
    category    = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'missions'


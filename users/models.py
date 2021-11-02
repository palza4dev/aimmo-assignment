from django.db import models

class User(models.Model):

    name       = models.CharField(max_length=50)
    email      = models.EmailField(max_length=100, unique=True)
    password   = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = 'users'
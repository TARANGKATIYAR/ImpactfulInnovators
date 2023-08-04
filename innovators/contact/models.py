from django.db import models

# Create your models here.
class contact(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.TextField()

    def __str__(self):
        return self.firstname
    
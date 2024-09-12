from django.db import models

# Create your models here.
class Candidate(models.Model):
    first_name = models.CharField(max_length=60)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)

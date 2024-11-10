from django.db import models

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    expiration_date = models.CharField(max_length=50)

    def __str__(self):
        return self.name


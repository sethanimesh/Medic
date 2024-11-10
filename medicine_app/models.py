from django.db import models

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    expiration_date = models.DateField()

    def __str__(self):
        return self.name

class MedicineScan(models.Model):
    image = models.ImageField(upload_to='medicine_scans/')
    processed_image = models.ImageField(upload_to='processed_scans/', null=True, blank=True)
    detections = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan {self.id} at {self.uploaded_at}"
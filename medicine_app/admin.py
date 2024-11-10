from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Medicine, MedicineScan

admin.site.register(Medicine)
admin.site.register(MedicineScan)
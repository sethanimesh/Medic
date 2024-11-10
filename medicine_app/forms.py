from django import forms
from .models import Medicine, MedicineScan

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'manufacturer', 'dosage', 'expiration_date']

class MedicineScanForm(forms.ModelForm):
    class Meta:
        model = MedicineScan
        fields = ['image']
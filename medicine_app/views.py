# Create your views here.
from django.shortcuts import render, redirect

from medicine_app.models import Medicine
from .forms import MedicineForm

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'medicine_app/add_medicine.html', {'form': form})

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_app/medicine_list.html', {'medicines': medicines})
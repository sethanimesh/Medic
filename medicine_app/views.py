# medicine_app/views.py

from django.shortcuts import render, redirect
from .forms import MedicineForm, MedicineScanForm
from .models import Medicine, MedicineScan
from ultralytics import YOLO
import cv2
import os
from django.conf import settings
from django.core.files.base import ContentFile
import base64
import json

# Load the YOLOv8 model (use a pre-trained model or your custom model)
model = YOLO('yolov8n.pt')  # Replace with your custom model path if available

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

def scan_medicine(request):
    if request.method == 'POST':
        form = MedicineScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save()

            # Perform detection
            image_path = scan.image.path
            detections, processed_image_path = detect_medicine(image_path)

            # Save processed image and detections
            with open(processed_image_path, 'rb') as f:
                processed_image_content = ContentFile(f.read())
                scan.processed_image.save(os.path.basename(processed_image_path), processed_image_content, save=False)

            scan.detections = detections
            scan.save()

            return redirect('scan_result', scan_id=scan.id)
    else:
        form = MedicineScanForm()
    return render(request, 'medicine_app/scan_medicine.html', {'form': form})

def scan_result(request, scan_id):
    scan = MedicineScan.objects.get(id=scan_id)
    return render(request, 'medicine_app/scan_result.html', {'scan': scan})

def scan_history(request):
    scans = MedicineScan.objects.all().order_by('-uploaded_at')
    return render(request, 'medicine_app/scan_history.html', {'scans': scans})

def live_feed(request):
    if request.method == 'POST':
        form = MedicineScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save()

            # Perform detection
            image_path = scan.image.path
            detections, processed_image_path = detect_medicine(image_path)

            # Save processed image and detections
            with open(processed_image_path, 'rb') as f:
                processed_image_content = ContentFile(f.read())
                scan.processed_image.save(os.path.basename(processed_image_path), processed_image_content, save=False)

            scan.detections = detections
            scan.save()

            return render(request, 'medicine_app/scan_result.html', {'scan': scan})
    else:
        form = MedicineScanForm()
    return render(request, 'medicine_app/live_feed.html', {'form': form})

def detect_medicine(image_path):
    """
    Perform object detection on the given image, draw bounding boxes, and save the processed image.
    Returns the detection details and the path to the processed image.
    """
    results = model(image_path)
    result = results[0]

    # Open the image with OpenCV
    img = cv2.imread(image_path)

    detections = []
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        conf = box.conf[0].cpu().numpy()
        cls = int(box.cls[0].cpu().numpy())
        label = model.names[cls]

        detections.append({
            'label': label,
            'confidence': round(float(conf), 2),
            'bbox': [x1, y1, x2, y2]
        })

        # Draw bounding box and label on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Save the processed image
    processed_image_name = f"processed_{os.path.basename(image_path)}"
    processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed_scans', processed_image_name)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(processed_image_path), exist_ok=True)

    cv2.imwrite(processed_image_path, img)

    return detections, processed_image_path
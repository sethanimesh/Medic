# medicine_app/views.py
import re
import base64
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from medicine_app.forms import MedicineForm
from medicine_app.models import Medicine
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# Initialize Vertex AI
vertexai.init(project="stalwart-city-431506-n8", location="us-central1")

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_app/medicine_list.html', {'medicines': medicines})

def generate(image_data):
    model = GenerativeModel("gemini-1.5-flash-002")
    
    # Convert image data to the correct format (base64)
    image_base64 = base64.b64decode(image_data)
    image_part = Part.from_data(mime_type="image/jpeg", data=image_base64)

    text1 = """You are a helpful assistant that can extract information from images of medicine bottles. You will be provided with an image of a medicine bottle. Extract the name, manufacturer, dosage, and expiration date of the medicine from the image."""
    
    text2 = """Output the extracted information in the following format:
    Name: [Medicine name]
    Manufacturer: [Manufacturer name]
    Dosage: [Dosage information]
    Expiration Date: [Expiration date]"""

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.OFF),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.OFF),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.OFF),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.OFF),
    ]
    
    # Generate content using the model
    responses = model.generate_content(
        [text1, image_part, text2],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_text = ""
    for response in responses:
        response_text += response.text

    return response_text

def capture_medicine_image(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON body
            data = json.loads(request.body.decode('utf-8'))
            image_data = data.get('image')  # Get base64 encoded image data

            if image_data:
                response_text = generate(image_data)
                
                # Parse the response using regex
                parsed_data = parse_response(response_text)
                
                if parsed_data:
                    # Save the parsed data to the database
                    medicine = Medicine(
                        name=parsed_data.get('Name'),
                        manufacturer=parsed_data.get('Manufacturer'),
                        dosage=parsed_data.get('Dosage'),
                        expiration_date=parsed_data.get('Expiration Date')
                    )
                    medicine.save()
                    
                    # Optionally, you can also create a MedicineForm instance if needed
                    # form = MedicineForm(parsed_data)
                    # if form.is_valid():
                    #     form.save()
                    
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({"error": "Failed to parse medicine details."}, status=400)
            else:
                return JsonResponse({"error": "Image data is missing"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def live_feed(request):
    return render(request, 'medicine_app/live_feed.html')



def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')  # Redirect to the medicine list after adding
    else:
        form = MedicineForm()
    return render(request, 'medicine_app/add_medicine.html', {'form': form})

# medicine_app/views.py

def parse_response(response_text):
    """
    Parses the Vertex AI response to extract medicine details using regex.
    
    Expected response format:
    Name: Ibuprofen Tablets I.P. BRUFEN 400
    Manufacturer: Abbott India Limited
    Dosage: 400 mg
    Expiration Date: 4/2024
    """
    try:
        # Define regex patterns for each field
        name_pattern = r"Name:\s*(.*)"
        manufacturer_pattern = r"Manufacturer:\s*(.*)"
        dosage_pattern = r"Dosage:\s*(.*)"
        expiration_pattern = r"Expiration Date:\s*(.*)"

        # Use re.MULTILINE to search across multiple lines
        name_match = re.search(name_pattern, response_text, re.MULTILINE)
        manufacturer_match = re.search(manufacturer_pattern, response_text, re.MULTILINE)
        dosage_match = re.search(dosage_pattern, response_text, re.MULTILINE)
        expiration_match = re.search(expiration_pattern, response_text, re.MULTILINE)

        # Extract the matched groups
        name = name_match.group(1).strip() if name_match else None
        manufacturer = manufacturer_match.group(1).strip() if manufacturer_match else None
        dosage = dosage_match.group(1).strip() if dosage_match else None
        expiration_date = expiration_match.group(1).strip() if expiration_match else None

        # Check if all fields are extracted
        if all([name, manufacturer, dosage, expiration_date]):
            return {
                "Name": name,
                "Manufacturer": manufacturer,
                "Dosage": dosage,
                "Expiration Date": expiration_date
            }
        else:
            return None

    except Exception as e:
        # Log the exception if needed
        print(f"Error parsing response: {e}")
        return None
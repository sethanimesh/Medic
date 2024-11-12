
# Medicine Manager

## Overview
Medicine Manager is a Django-based web application designed for efficient management of medicine records. 
It uses a combination of Django’s powerful backend framework, a responsive frontend built with Bootstrap, 
and Google Vertex AI for intelligent image analysis. This application streamlines the process of cataloging 
and managing medicine details, making it suitable for pharmacies, healthcare providers, and personal use.

## Features
- **Medicine Cataloging**: Add, view, edit, and delete medicine records.
- **Live Webcam Capture**: Capture medicine images directly from the app using a live webcam feed.
- **AI-Powered Extraction**: Leverages Google Vertex AI to automatically extract medicine details like name, 
  manufacturer, dosage, and expiration date from captured images.
- **User-Friendly Interface**: Responsive design using Bootstrap, including interactive elements such as modals 
  and loader animations.

## Tech Stack

### Backend
- **Django**: Handles the backend logic, data validation, and database management.

### Frontend
- **HTML5, CSS3, JavaScript**: Provides structure, styling, and dynamic interactions.
- **Bootstrap 5**: Ensures a responsive and mobile-friendly interface.

### AI & Image Processing
- **Google Vertex AI**: Performs image analysis to extract medicine information from bottle images.

### Database
- **SQLite (Development)** / **PostgreSQL/MySQL (Production)**: Stores and manages medicine records.

## Setup and Installation

### Prerequisites
- Python 3.x
- Django 4.x
- Google Cloud account (for Vertex AI integration)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/sethanimesh/medic.git
   cd medicine-manager
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Google Vertex AI:
   - Set up Google Cloud credentials and enable Vertex AI API.
   - Update the Vertex AI project and location settings in `views.py`.

5. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

7. Access the app at `http://127.0.0.1:8000`.

## Usage
1. **Add Medicine**: Capture an image of the medicine using the live feed or add details manually.
2. **View Medicines**: Access a list of all medicines, displaying key details.
3. **Edit/Delete Medicines**: Update or remove medicine entries directly from the list.

## Folder Structure
```plaintext
medicine-manager/
├── medicine_app/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   └── ...
├── medicine_project/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── README.md
```

## Contributing
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

---

**Medicine Manager** simplifies the process of managing medicinal information, utilizing AI to automate 
data extraction, and Django for a solid backend. This project is perfect for pharmacies, healthcare 
facilities, or anyone needing efficient medicine management.

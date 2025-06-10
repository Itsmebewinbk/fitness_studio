
---

````markdown
# 🧘 Fitness Studio Booking API

A Django-based REST API to manage fitness class bookings, created as part of a Python Developer Assignment.

---

## 📌 Features

- View all upcoming fitness classes
- Book a class with client details
- List all bookings by client email
- Prevents overbooking and past bookings
- Timezone-aware (IST)
- Clean, modular code using Django REST Framework

---

## 🛠️ Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- SQLite (in-memory or file-based)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Itsmebewinbk/fitness_studio
cd fitness_studio
````

### 2. Create virtual environment and activate

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, manually install dependencies like this:

```bash
pip install django djangorestframework django-filter drf-yasg python-decouple
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

---

## 📬 API Endpoints

### ✅ GET `/classes/`

List all upcoming fitness classes.

```bash
curl http://localhost:8000/api/v1/classes/
```

---

### ✅ POST `/book/`

Book a class with client name and email.

**Sample Request JSON:**

```json
{
  "class_id": 1,
  "client_name": "Test",
  "client_email": "testn@gmail.com"
}
```

```bash
curl -X POST http://localhost:8000/api/v1/book/ \
  -H "Content-Type: application/json" \
  -d '{"class_id": 1, "client_name": "Test", "client_email": "test@gmail.com"}'
```

---

### ✅ GET `/bookings/?email=test@gmail.com`

List all bookings for a specific client email.

```bash
curl http://localhost:8000/api/v1/bookings/?email=test@example.com
```

---

## 🕒 Timezone Handling

* All datetimes are stored in IST (Asia/Kolkata)
* Prevents booking of past events (relative to IST)
* Uses Django timezone utilities internally

---



## ✅ Running Tests

Run unit tests with:

```bash
python manage.py test
```

Tests cover:

* Class listing
* Successful bookings
* Booking errors (full/past classes)
* Filtering bookings by email

---

## 📁 Project Structure

```
fitness_studio/
├── fitness_booking/
│   ├── models.py         # FitnessClass & Booking models
│   ├── serializers.py    # Input/output validation
│   ├── views.py          # API views
│   ├── urls.py           # Route mappings
│   ├── filters.py        # Email filtering logic
│   └── tests.py          # Unit tests
├── fitness_studio/
│   ├── settings.py       # Django settings with timezone and logging
│   ├── urls.py           # Root URL config
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📽️ Video Demo

🎥 [Click here to watch the Loom demo](https://drive.google.com/file/d/14JlrD0v3D_J0vkZ0OGTiGCjn1dm7Ygp0/view)

---

## 👤 Author

**Bewin Babu**

* 🔗 [GitHub](https://github.com/Itsmebewinbk)
* 🔗 [LinkedIn](https://www.linkedin.com/in/bewin-babu-150405170/)

---


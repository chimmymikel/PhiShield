# PhiShield - Phishing Detection System

A Django-based web application designed to detect and prevent phishing attacks by analyzing URLs and messages in real-time. PhiShield helps users identify suspicious links, scan emails, and monitor their security history through an intuitive dashboard.

## Features

- 🔍 **URL Analysis**: Scan suspicious links for phishing attempts
- 📧 **Message Scanning**: Analyze emails and messages for phishing content  
- 🛡️ **Real-time Protection**: Instant threat detection
- 📊 **Security Dashboard**: Monitor protection history
- 👥 **User Authentication**: Secure login and registration system

## Technology Stack

- **Backend**: Django 5.2.7
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite3
- **Authentication**: Django Auth System

## Installation & Setup

1. Clone the repository:
```
git clone https://github.com/chimmymikel/PhiShield.git
cd PhiShield
```

2. Create a virtual environment:
```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py migrate
```

5. Create a superuser (optional):
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## Team Members

### Development Team
- **Michelle Marie P. Habon** (Lead Developer) - michellemarie.habon@cit.edu
- **Adrian V. Hernandez** (Backend Developer) - adrian.hernandez@cit.edu
- **Gave C. Hontiveros** (Frontend Developer) - gave.hontiveros@cit.edu

### Project Management Team
- **Jac Gary F. Cañete** (Product Owner) - jacgary.canete@cit.edu
- **Joseph Harry G. Butihen** (Business Analyst) - josephharry.butihen@cit.edu
- **Reenah Mae R. Campilanan** (Scrum Master) - reenahmae.campilanan@cit.edu

## Deployed Link
**Live Application**: https://csit327-g8-phishield-production.up.railway.app/

---

**PhiShield** - Protecting you from phishing threats, one click at a time.

# 🏥 Therapy Management System

## 📌 Project Overview

Therapy Management System is a full-stack database-driven web application designed to streamline the management of therapy-related records. It allows healthcare administrators and clinicians to maintain patient details, schedule therapy sessions, record assessments, and track treatment logs efficiently.

The system provides an intuitive web interface with secure database connectivity and complete CRUD functionality.

---

## ✨ Key Features

### 👤 Patient Management
- Add new patients with personal details
- View patient records
- Update patient information
- Delete patient records and associated therapy data

### 👨‍⚕️ Clinician Management
- Register clinicians with specialization details
- View available clinicians
- Edit clinician information
- Remove clinician records

### 📅 Therapy Session Management
- Schedule therapy sessions
- Assign patients to clinicians
- Maintain session dates and treatment notes
- View complete session history

### 📊 Assessment Management
- Record patient assessments
- Store assessment type, score, and remarks
- Track progress across therapy sessions

### 📝 Treatment Log Management
- Maintain detailed therapy logs
- Record session activities and observations
- Track historical treatment information

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- PyMySQL

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- MySQL

---

## 📁 Project Structure

```
Therapy-Management-System
│
├── static/                 # CSS, JavaScript, and assets
│
├── templates/              # HTML templates
│
├── app.py                  # Main Flask application
├── routes.py               # Application routes
├── models.py               # Database models
├── config.py               # Database configuration
├── database.db             # Database files/configuration
│
└── instance/               # Application instance data
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dbms.git
```

### 2. Navigate to the Project Folder

```bash
cd dbms
```

### 3. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux/Mac**
```bash
source venv/bin/activate
```

### 4. Install Required Packages

```bash
pip install flask pymysql
```

### 5. Configure MySQL Database

Create a MySQL database named:

```
therapy_db
```

Update the database credentials in `app.py` or configuration files with your MySQL username and password.

### 6. Run the Application

```bash
python app.py
```

The Flask server will start at:

```
http://127.0.0.1:5000
```

Open the URL in your browser.

---

## 🗄️ Database Entities

The system maintains the following major entities:

- Patients
- Clinicians
- Therapy Sessions
- Assessments
- Treatment Logs

The entities are connected using relational database concepts such as primary keys, foreign keys, and one-to-many relationships.

---

## 🎯 Project Objectives

- To automate and simplify therapy record management.
- To maintain structured patient and clinician databases.
- To provide efficient tracking of therapy sessions and assessments.

---

## 🔮 Future Enhancements

- User authentication and role-based access
- Appointment reminders and notifications
- Report generation in PDF format
- Data analytics for patient progress
- Cloud-based database integration

---

## 👩‍💻 Developer

Developed by **Sanjana Shetty**

---

## 📄 License

This project is developed for educational and academic purposes.

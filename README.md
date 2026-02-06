🏥 E-Hospitality — Healthcare Management System

A full-stack Hospital Management Web Application built using Django that connects Patients, Doctors, and Administrators in one integrated healthcare platform.

This system streamlines hospital operations including patient registration, appointment booking, doctor management, and administrative control.

🚀 Project Overview

E-Hospitality is designed to digitalize hospital workflows and reduce manual paperwork. The system provides:

✔ Secure authentication
✔ Role-based access
✔ Appointment management
✔ Doctor onboarding
✔ Admin monitoring dashboard

It simulates how real hospitals manage users, staff, and appointments.

👥 User Roles
🧑‍🤝‍🧑 Patient

Register account

Login securely

Book appointments

View personal dashboard

Manage health interactions

🩺 Doctor

Login (credentials created by Admin)

View assigned appointments

Manage patient consultations

Access doctor dashboard

🛠 Admin

Login as admin/superuser

Add doctors to system

Approve doctors

Monitor users and appointments

Manage hospital departments

View system statistics

✨ Key Features
Feature	Description
🔐 Authentication System	Secure login/logout using Django auth
👤 Role-Based Access	Separate dashboards for Patient, Doctor, Admin
🧾 Patient Registration	Patients can self-register
🩺 Doctor Creation	Admin registers doctors
📅 Appointment Booking	Patients book appointments with doctors
📊 Admin Dashboard	View stats: users, doctors, patients, appointments
⛔ Access Control	Unauthorized users blocked from restricted pages
🔄 Redirect Logic	Automatic dashboard redirection after login
🚫 Cache Prevention	Prevents back-button misuse after logout
🎨 Modern UI	Bootstrap + custom styling
🏗 Tech Stack
Layer	Technology
Backend	Django (Python)
Frontend	HTML, CSS, Bootstrap, JavaScript
Database	SQLite (can be changed to MySQL/PostgreSQL)
Authentication	Django Authentication System
Styling	Bootstrap 5 + Custom CSS
📂 Project Structure (Simplified)
ehospitality/
│
├── accounts/        → User model, login, registration
├── patient/         → Patient dashboard & appointments
├── doctor/          → Doctor dashboard & views
├── adminpanel/      → Admin dashboard & management
├── templates/       → HTML templates
├── static/          → CSS, JS, images
└── manage.py

🔐 Authentication Flow
Role	How Account is Created
Patient	Self-registration
Doctor	Created by Admin
Admin	Created via Django superuser
📌 Important Security Measures

✔ CSRF protection
✔ Role validation on login
✔ Approval check for doctors
✔ Prevents form resubmission
✔ Cache disabled on secure pages
✔ Back button protection after logout

⚙ Installation Steps
# Clone repository
git clone https://github.com/yourusername/ehospitality.git

# Move into project
cd ehospitality

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Create admin
python manage.py createsuperuser

# Run server
python manage.py runserver


Visit:

http://127.0.0.1:8000/

📸 System Modules

Patient Registration Module

Doctor Login Module
Doctor Login Module

Admin Dashboard

Appointment Booking System

Department Management

🎯 Purpose of Project

This project demonstrates:

✔ Full-stack web development
✔ Django authentication
✔ Role-based system design
✔ Real-world hospital workflow modeling
✔ Secure web practices


🔑 Demo Login Credentials (For Testing)

⚠️ These are sample accounts for demonstration. Change passwords in production.

Role	Username	Password
🛠 Admin	Adminmeena	Admin@123 (example)
🧑‍🤝‍🧑 Patient	meena	Patient@123 (example)
🩺 Doctor	Created by admin	Provided during doctor creation

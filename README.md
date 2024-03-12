# A comprehensive hospital management system
### Ojectives:
- To create a hospital management system that simplifies multi-hospital control and registration for founders.
- To implement role-based access control for efficient administration, appointments, and prescription management.
- To enhance user experience with a user-friendly interface and comprehensive medical test and medicine lists.
- To ensure data security and scalability while encouraging community contributions for ongoing development.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Features](#features)
- [Roles](#roles)
- [User Profiles](#user-profiles)
- [Appointments](#appointments)
- [Prescriptions](#prescriptions)
- [Medical Tests](#medical-tests)
- [Medicine List](#medicine-list)


### Introduction
The "Multi-Vendor Hospital Management" project is a robust and versatile hospital management system designed to streamline and enhance the operations of healthcare institutions, doctors, and patients. With multi-vendor support, user roles, and an array of features, this system offers a comprehensive solution for managing hospitals, appointments, and medical data.

### Installation

1. Clone the repository:
  ```
    git clone https://github.com/Parvez49/Multi-Vendor-Hospital-Management.git
  ```
2. Create a Virtual Environment and install Dependencies:
   ```
      python -m venv venv
      pip install -r requirements.txt
   ```
3. Run Migrations:
   Make sure your postgres database environment settings in .env:
   ```
     # Postgres Database
      DB_NAME=MultiVendorHospital
      DB_USER=postgres
      DB_PASS=admin
      DB_HOST=127.0.0.1
      PORT=5432
   ```
   Now migrate:
   ```
     python manage.py migrate
   ```
5. Start the development server:
   ```
     python manage.py runserver
   ```
6. Note: Your project should run successfully. However, you might encounter issues if Redis and Celery servers are not running as per the environment settings. Configure Redis and Celery settings in the .env file:
   ```
     # Celery 
     CELERY_BROKER_URL=redis://127.0.0.1:6379/0
     CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
    
     # Cache
     CACHE_URL=redis://127.0.0.1:6379/1
   ```
    To start the Redis server:
   ```
        redis-server
   ```
    To start the Celery worker and Celery beat (in separate terminals):
   ```
         # Make sure your terminal location is where manage.py is located
         celery worker: celery -A Multi_Vendor_Hospital_System worker --loglevel=info
         celery beat: celery -A Multi_Vendor_Hospital_System beat
   ```













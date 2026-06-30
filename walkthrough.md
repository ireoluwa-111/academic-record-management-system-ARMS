# Walkthrough - Academic Record Management System (ARMS) Integration

We have successfully rewired the prototype, replacing all hardcoded mockup screens with a robust Django backend database integration. The project is fully complete and operational.

## Changes Made

### 1. Django App and Configurations
- Created a new Django app named [records](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/records) to manage the backend business logic.
- Registered `records` and `corsheaders` in [settings.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/config/settings.py).
- Configured custom auth model `AUTH_USER_MODEL = 'records.User'` in settings.
- Configured settings `TEMPLATES` `DIRS` to point to `/templates` and `STATICFILES_DIRS` to point to `/static` directory in the root.
- Set `LOGIN_URL = 'login'` to handle login redirections.
- Configured main routing in [urls.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/config/urls.py) to forward to `records/urls.py`.

### 2. Database Schema
Defined 6 database models in [models.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/records/models.py):
1. **User (extends AbstractUser)**: Includes customized fields (`role`, `reg_id` for Matric/Staff ID, `department`, `level`, `programme`, `session`, `status`).
2. **Department**: Standard code (e.g. `CSC`) and department name.
3. **Course**: Code (e.g. `CSC 301`), title, units (credits), department, lecturer, and semester.
4. **Enrollment**: Links students to registered courses, tracking score (0-100), automated grade conversion, and approval status.
5. **TranscriptRequest**: Tracks student requests for official transcript generation.
6. **AuditLog**: Automates logging of critical system events (logins, registrations, grade updates, approvals).

### 3. Frontend Restructuring
- Assets (CSS and JS folders) were copied from `/frontend` to `/static` directory in the root.
- All prototype mockup HTML pages were copied to `/templates` directory in the root.
- Adjusted relative asset paths inside templates to point to `/static/css/...` and `/static/js/...`.

### 4. Dynamic Templates Integration
- **Index**: Wired dynamic statistics counters showing database-driven student, course, and transcript totals.
- **Login & Register**: Hooked forms to Django POST handlers with CSRF tokens and automated error notifications.
- **Student Dashboard**: 
  - Dynamic GPA and CGPA calculation.
  - Interactive SVG GPA ring that draws progress based on active CGPA.
  - Real registered courses table mapping statuses ("Enrolled", "Pending approval").
  - Dynamically populated recent activity audit logs.
  - Added a Course Registration modal popup showing unregistered department courses.
- **Lecturer Dashboard**:
  - Live summaries of teaching courses, enrolled student counts, and pending scores.
  - Grade entry queue table showing student numbers and average scores.
  - Result entry modals for each course letting the lecturer save scores which automatically map to letter grades (A, B, C, D, E, F).
- **Registrar Dashboard**:
  - Student record database listing actual students, levels, program, and dynamic CGPA.
  - Pending registration oversight approvals table allowing registrar to check/approve registration requests.
  - Pending transcript requests table showing approval actions.
  - Live registry audit trails list showing system updates.
- **Admin Dashboard**:
  - Lists users, departments, and live system log trails.
  - Modal form to register new users (Students, Lecturers, Registrars, Admins).
  - Status management dropdowns to suspend or change user standings.
- **Official Transcript (Print View)**:
  - Generates a certificate style page of a student's full academic records, grouping courses chronologically by session and semester.
  - Computes exact semester GPAs and cumulative CGPA.
  - Standardized print-friendly CSS so clicking "Print Transcript" formats cleanly to standard paper layout or downloads as a PDF.

---

## Seeding & Mockup Continuity

We created a database seeding script [seed.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/seed.py) containing all mockup accounts and records to ensure transition is immediate and seamless:
- **Student Demo**: login with `CSC/2022/0417` or email `a.okoro@university.edu`, password `password123`.
- **Lecturer Demo**: login with `t.okafor` or email `t.okafor@university.edu`, password `password123`.
- **Registrar Demo**: login with `f.bello` or email `f.bello@university.edu`, password `password123`.
- **Admin Demo**: login with `s.adeyemi` or email `s.adeyemi@university.edu`, password `password123`.

To support immediate logins on the auth screens, the quick actions "Student demo" and "Registrar demo" on the login screen were rewired to log in the seeded accounts automatically using dynamic session logic.

---

## Verification

### Automated Tests
We wrote unit tests in [tests.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/records/tests.py) validating:
1. Student GPA/CGPA calculations.
2. Automated grade and point mappings.
3. Route access restriction (anonymous users redirect to `/login/`).

All tests pass:
```bash
.\venv\Scripts\python manage.py test records
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 6.548s

OK
Destroying test database for alias 'default'...
```

### Run Project Locally
To run and inspect the project:
1. Start the server:
   ```bash
   .\venv\Scripts\python manage.py runserver
   ```
2. Navigate to `http://localhost:8000/` in your browser.
3. Access dashboards using either the form logins or the quick-action demo buttons on `/login/`.

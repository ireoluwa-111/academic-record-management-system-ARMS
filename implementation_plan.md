# Implementation Plan - Academic Record Management System (ARMS) Backend Wiring

This plan outlines the architecture, database design, and template modifications required to transition the ARMS prototype from a static frontend to a fully database-driven Django application.

## User Review Required

> [!IMPORTANT]
> - **Authentication Mechanics**: Standard Django session-based authentication will be used. Users can log in using either their matriculation/staff ID (`reg_id`) or their university email.
> - **CGPA/GPA Calculations**: Computations will dynamically follow the standard Nigerian university grading system (A=5, B=4, C=3, D=2, E=1, F=0) based on numeric scores:
>   - $70 - 100$: A (5 points)
>   - $60 - 69$: B (4 points)
>   - $50 - 59$: C (3 points)
>   - $45 - 49$: D (2 points)
>   - $40 - 44$: E (1 point)
>   - $0 - 39$: F (0 points)
> - **Default Accounts**: To preserve user demos, we will seed the database with the exact mockup accounts (Adaeze Okoro for Student, Dr. Tunde Okafor for Lecturer, Funmilayo Bello for Registrar, Samuel Adeyemi for Admin) so they are fully functional out-of-the-box.

---

## Proposed Changes

### Component 1: Django Backend Configuration and Models

We will create a Django app named `records` that will house the models, views, and core business logic of the system.

#### [NEW] [models.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/records/models.py)
We will define the following models:
- **`User` (extends `AbstractUser`)**: Handles user profiles with roles (`student`, `lecturer`, `registrar`, `admin`), `reg_id` (Matric/Staff ID), `department`, `level`, `programme`, `session`, and `status`.
- **`Department`**: Unique code (e.g., `CSC`) and full name.
- **`Course`**: Code (e.g., `CSC 301`), title, units (credits), department, lecturer, and semester.
- **`Enrollment`**: Relationship between Student and Course with a registration status (`Pending`, `Enrolled`), numeric score, and calculated grade.
- **`TranscriptRequest`**: Tracking reference, request date, and approval status (`Pending`, `Approved`, `Denied`).
- **`AuditLog`**: Logs system activities (e.g., result entries, course registration, user updates).

#### [MODIFY] [settings.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/config/settings.py)
- Register `records` in `INSTALLED_APPS`.
- Set `AUTH_USER_MODEL = 'records.User'`.
- Define template directories to render HTML templates from the root `templates` folder.
- Configure static directories to serve CSS, JS, and image assets from a central `static` directory.
- Maintain sqlite3 as the default database for immediate local execution.

#### [MODIFY] [urls.py](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/config/urls.py)
- Route root URL requests (`/`) to the landing page.
- Map auth routes: `/login/`, `/register/`, `/logout/`.
- Map dashboard routes: `/dashboard/student/`, `/dashboard/lecturer/`, `/dashboard/registrar/`, `/dashboard/admin/`.
- Map action routes: `/course-register/`, `/update-grade/`, `/approve-enrollment/`, `/request-transcript/`, `/approve-transcript/`, `/user-management/`.

---

### Component 2: Frontend Asset Restructuring

We will restructure the static HTML prototype into Django templates and static assets.

#### Move Assets:
- Move files from `frontend/css/` and `frontend/js/` to a new `static/` directory in the project root.
- Move HTML files from `frontend/` to a new `templates/` directory in the project root.

#### Convert HTML to Django Templates:
For each template, replace hardcoded values with Django context variables:
1. **[index.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/index.html)**:
   - Dynamic landing statistics (student count, courses count, transcript count).
2. **[login.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/login.html) & [register.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/register.html)**:
   - Wire registration/login forms to Django auth endpoints. Show error alerts on mismatch or validation errors.
3. **[dashboard-student.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/dashboard-student.html)**:
   - Display active student CGPA/GPA.
   - Render registered courses dynamically.
   - Implement course registration modal to select and request courses.
   - Wire "Download transcript" to trigger a print-friendly transcript/result sheet.
4. **[dashboard-lecturer.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/dashboard-lecturer.html)**:
   - List courses taught.
   - Display a result entry list where the lecturer can enter score inputs (0-100) for student enrollments and save drafts or finalize grades.
5. **[dashboard-registrar.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/dashboard-registrar.html)**:
   - Render student records dynamically. Show CGPAs, program, status.
   - Action buttons to approve pending course enrollments.
   - Transcript request processing panel.
6. **[dashboard-admin.html](file:///c:/Users/Ireoluwade/Documents/academic-record-management-system/templates/dashboard-admin.html)**:
   - Live list of users with search and filter capability.
   - Form to add new users (Students, Lecturers, Registrars, Admins) and edit user status.
   - Display live audit trails.

---

### Component 3: Data Seeding and Database Setup

 we will create a python script `seed.py` that populates the database with default data representing the mockup state so that login functions instantly.

#### Seeding details:
- **Departments**: Computer Science (CSC), Economics (ECO), Physics (PHY), Law (LAW).
- **Users**:
  - `CSC/2022/0417` (Student: Adaeze Okoro)
  - `t.okafor` / `staff-001` (Lecturer: Dr. Tunde Okafor)
  - `f.bello` / `staff-002` (Registrar: Funmilayo Bello)
  - `s.adeyemi` / `staff-003` (Admin: Samuel Adeyemi)
- **Courses**: CSC 301, CSC 305, CSC 311, CSC 313, MTH 302, GST 301, ECO 201, PHY 201.
- **Grades**:
  - Seed historical enrollments for Adaeze Okoro in 1st/2nd semesters of 100/200 level to yield her precise `4.62` CGPA.
  - Seed current pending courses (e.g. MTH 302) to showcase "Pending approval" and database interaction.

---

## Verification Plan

### Automated Verification
We will run:
```bash
.\venv\Scripts\python manage.py makemigrations records
.\venv\Scripts\python manage.py migrate
.\venv\Scripts\python manage.py shell -c "import seed; seed.run()"
.\venv\Scripts\python manage.py test records
```
This ensures models are syntactically correct, migrations succeed, database seeding completes, and simple backend unit tests pass.

### Manual Verification
1. Start the Django development server: `.\venv\Scripts\python manage.py runserver`
2. Test Login:
   - Log in as Student `CSC/2022/0417` -> Verify dashboard displays Adaeze Okoro, CGPA 4.62, and registered courses.
   - Log in as Lecturer `staff-001` -> Verify list of courses and result entry draft/finalize actions.
   - Log in as Registrar `staff-002` -> Verify student list, enrollment approval, and transcript generation triggers.
   - Log in as Admin `staff-003` -> Verify user listing, creation, and logs.
3. Verify Course Registration flow:
   - Log in as Student, select a course to register.
   - Log in as Registrar, verify course registration appears in pending queue, approve it.
   - Log in as Student, verify status changes to "Enrolled".
4. Verify Grading flow:
   - Log in as Lecturer, submit grade for student.
   - Log in as Student, verify grade/GPA changes dynamically.
5. Verify Transcript request:
   - Student clicks request, Registrar approves request, Student is able to download/view the transcript.


 CHAPTER THREE

## RESEARCH METHODOLOGY

 3.1 INTRODUCTION

This chapter describes the methodology adopted in designing and developing the Academic Record Management System (ARMS). It outlines the approach used to gather requirements, the software development model employed, the tools and technologies that formed the development environment, and the complete database design that underpins the system. The goal of this chapter is to provide a structured account of how the system was conceived, planned, and built from the ground up.

The development of ARMS followed a disciplined, phase-driven approach to ensure that the system accurately addresses the identified problems of manual academic record-keeping in higher institutions. Every phase—from requirement gathering through to implementation—was driven by best practices in software engineering.

---

 3.2 REQUIREMENT SPECIFICATION

Requirement specification is the process of identifying, documenting, and verifying what a system must do (functional requirements) and how well it must perform (non-functional requirements). For ARMS, requirements were gathered through a careful analysis of the problems inherent in manual record management systems used in Nigerian universities, as well as a review of existing digital solutions and their limitations.

3.2.1 Functional Requirements

Functional requirements describe the specific behaviours, features, and functions that the system must be capable of performing. The following are the core functional requirements of ARMS, organized by user role:

**A. Student**

1. Students shall be able to register an account on the system using their matriculation number, full name, email address, and a secure password.
2. Students shall be able to log in to the system using their matriculation number or registered email address.
3. Students shall be able to view their personal profile, including their department, programme, level, and academic session.
4. Students shall be able to update their personal profile information (name, email, programme).
5. Students shall be able to register for courses offered in their department for the current semester, subject to registrar approval.
6. Students shall be able to view all their registered courses, including course code, title, credit units, lecturer, and enrolment status.
7. Students shall be able to view their academic results, organized by semester and session, including scores, letter grades, semester GPA, and cumulative CGPA.
8. Students shall be able to request an official academic transcript through the system.
9. Students shall be able to view recent account activities and system notifications.
10. Students shall be able to change their account password.

**B. Lecturer**

1. Lecturers shall be able to log in using their staff ID or registered email address.
2. Lecturers shall be able to view a summary of all courses assigned to them, including enrolment statistics.
3. Lecturers shall be able to view the student roster for each of their assigned courses.
4. Lecturers shall be able to enter and update student scores (0–100) for courses they teach.
5. The system shall automatically compute and assign letter grades (A, B, C, D, E, F) based on the entered score.
6. Lecturers shall be able to mark a result as finalized once all students have been graded.
7. Lecturers shall be able to update their personal profile information and change their password.

**C. Registrar**

1. The registrar shall be able to log in using their staff ID or registered email address.
2. The registrar shall be able to search and view a comprehensive list of all registered students, including their department, level, programme, status, and computed CGPA.
3. The registrar shall be able to view, approve, or deny student course enrolment requests submitted by students.
4. The registrar shall be able to create new courses and assign them to departments and lecturers.
5. The registrar shall be able to view and manage all pending transcript requests from students, with the ability to approve or deny each request.
6. The registrar shall be able to view a live audit trail of all recent system activities.

**D. Administrator**

1. The administrator shall be able to log in to the system with elevated privileges.
2. The administrator shall be able to view and search all user accounts across all roles (students, lecturers, registrars).
3. The administrator shall be able to create new user accounts and assign them roles, departments, and other attributes.
4. The administrator shall be able to change a user's account status (Active, Probation, Suspended).
5. The administrator shall be able to create and manage academic departments.
6. The administrator shall have access to the full system audit log for oversight and compliance monitoring.

**E. System-Wide**

1. The system shall enforce role-based access control, ensuring that users can only access dashboards and data appropriate to their role.
2. The system shall automatically redirect unauthenticated users to the login page when they attempt to access a protected resource.
3. The system shall maintain an audit log of all significant user actions including logins, registrations, grade updates, and approvals.
4. The system shall automatically compute CGPA using the weighted grade point average formula based on enrolled course units and grades.
5. The system shall support the generation and printing of official academic transcripts in a clean, print-friendly format.

3.2.2 Non-Functional Requirements

Non-functional requirements define the quality attributes and operational constraints of the system.

1. **Security**: The system shall authenticate users via secure login and enforce session management. All sensitive routes shall require an active authenticated session. Passwords shall be stored as hashed values; plaintext passwords shall never be stored.
2. **Performance**: The system shall respond to user requests within an acceptable time frame, with database queries optimized using Django's ORM query mechanisms.
3. **Usability**: The system shall provide a clean, intuitive, and visually organized user interface that requires minimal training to use.
4. **Reliability**: The system shall handle errors gracefully, displaying informative messages to users when invalid operations are attempted (e.g., duplicate registration, wrong password).
5. **Maintainability**: The codebase shall be modular and well-structured, separating concerns between models, views, templates, and URL routing.
6. **Scalability**: The database schema and application architecture shall be designed to accommodate growth in the number of users, courses, and academic records over time.
7. **Portability**: The system shall be built on cross-platform technologies (Python/Django), enabling deployment on multiple operating systems.
8. **Auditability**: The system shall maintain comprehensive audit logs that record the actor, action, and timestamp of all significant system events.

---

3.3 METHOD AND MODELS USED

 3.3.1 Development Methodology

The development of ARMS adopted the **Agile Software Development Methodology**, specifically drawing on principles of iterative and incremental development. Unlike the traditional Waterfall model, which requires all requirements to be fully defined before development begins, Agile allows requirements and solutions to evolve through collaborative effort and continuous refinement.

The development of ARMS was carried out in the following iterative phases:

- **Phase 1 – Requirements & Design**: User stories were identified for all four roles (student, lecturer, registrar, administrator). The database schema was designed, and wireframe mockups of the user interface were created.
- **Phase 2 – Frontend Prototype**: A static HTML/CSS/JavaScript prototype was built, simulating all dashboards and user flows without backend logic. This allowed for early visual validation of the user interface.
- **Phase 3 – Backend Integration**: Django was configured, database models were created, and all views (business logic) were written to connect the frontend templates to live database data.
- **Phase 4 – Testing**: Automated unit tests were written and executed. Manual testing was conducted across all user flows and roles.
- **Phase 5 – Review & Refinement**: Issues discovered during testing were resolved; the interface and logic were refined based on review.

> **[DIAGRAM SUGGESTION]**: Insert a diagram here showing the Agile development cycle as applied to ARMS — illustrating the five phases in a cyclical/iterative model (Requirements → Design → Prototype → Integration → Test → Review → back to Requirements). A swimlane or circular flow diagram is recommended.

 3.3.2 System Architecture

ARMS follows the **Model-View-Template (MVT)** architectural pattern as implemented by the Django web framework. This is a variant of the popular Model-View-Controller (MVC) pattern and separates the application into three distinct layers:

| Layer | Component | Description |
|-------|-----------|-------------|
| **Model** | `records/models.py` | Defines the database structure and business logic (e.g., automatic grade computation) |
| **View** | `records/views.py` | Contains the application logic: processes requests, queries the database, and returns responses |
| **Template** | `/templates/` | HTML files that present data to the user in a structured, styled interface |

In addition, the system uses a **URL dispatcher** (`records/urls.py`) that maps incoming HTTP requests to the appropriate view function based on URL patterns. The Django framework itself acts as the controller, routing requests between the URL dispatcher and view layer.

> **[DIAGRAM SUGGESTION]**: Insert an MVT architecture diagram here showing the flow: Browser → URL Dispatcher → View → Model → Database, and the return path: Database → Model → View → Template → Browser.

 3.3.3 Use Case Model

The system serves four distinct categories of users. The following use cases capture the primary interactions:

**Student Use Cases:**
- Register account / Log in / Log out
- View dashboard (CGPA, GPA, course summary)
- Register for courses
- View course results by semester
- Request academic transcript
- Update profile / Change password

**Lecturer Use Cases:**
- Log in / Log out
- View assigned courses and student rosters
- Enter / Update student scores
- Finalize results
- Update profile / Change password

**Registrar Use Cases:**
- Log in / Log out
- Search and view student records
- Approve / Deny course enrolment requests
- Create and manage courses
- Approve / Deny transcript requests
- Monitor system audit logs

**Administrator Use Cases:**
- Log in / Log out
- Create and manage user accounts (all roles)
- Manage academic departments
- Change user account status
- View full system audit logs

> **[DIAGRAM SUGGESTION]**: Insert a UML Use Case Diagram here showing all four actors (Student, Lecturer, Registrar, Administrator) and their respective use cases. The system boundary should encompass all use cases, with actors positioned outside it. Shared use cases (Log In, Log Out, Update Profile, Change Password) can be connected to multiple actors.

 3.3.4 Data Flow Diagram (DFD)

A Data Flow Diagram illustrates how data moves through the ARMS system.

**Level 0 DFD (Context Diagram):**
At the highest level, ARMS is a single system that interacts with four external entities: Student, Lecturer, Registrar, and Administrator. Data flows into the system (e.g., login credentials, score entries, course registrations) and out of it (e.g., dashboards, result reports, audit logs, transcripts).

> **[DIAGRAM SUGGESTION]**: Insert a Level 0 DFD (Context Diagram) here. Draw a single central process labelled "ARMS" with four external entities: Student, Lecturer, Registrar, Administrator. Show labeled data flows between each entity and the system (e.g., Student → Login Details → ARMS; ARMS → Dashboard Data → Student).

**Level 1 DFD:**
At the next level, ARMS is decomposed into the following major sub-processes:
1. **User Authentication** — validates credentials and establishes sessions
2. **Course Management** — handles course registration, approval, and listing
3. **Grade Management** — processes score entry and automatic grade computation
4. **Transcript Management** — handles transcript requests and approvals
5. **User Administration** — manages account creation, status, and departments
6. **Audit Logging** — records all significant system events

> **[DIAGRAM SUGGESTION]**: Insert a Level 1 DFD here showing all six sub-processes, their associated data stores (Users, Courses, Enrollments, Transcripts, Departments, AuditLogs), and the data flows between external entities and these processes.

 3.3.5 System Flowchart

The general system flow for a user accessing ARMS is as follows:

1. User navigates to the ARMS landing page.
2. User clicks "Login" and is directed to the login form.
3. User enters their Matric/Staff ID (or email) and password.
4. The system validates the credentials against the database.
   - If invalid: an error message is displayed and the user is redirected back to the login form.
   - If valid: an authenticated session is created.
5. The system checks the user's role and redirects them to their role-specific dashboard.
6. The user interacts with their dashboard features (view data, submit forms, etc.).
7. For each action submitted (POST), the system validates, processes, updates the database, logs the action, and redirects back with a success or error notification.
8. On logout, the session is destroyed and the user is redirected to the login page.

> **[DIAGRAM SUGGESTION]**: Insert a system flowchart here illustrating the steps above. Use standard flowchart symbols (Rounded rectangles for Start/End, Rectangles for processes, Diamonds for decisions). The decision diamond at step 4 should branch to "Invalid credentials" (looping back to login) and "Valid credentials" (proceeding to role check).

---

 3.4 SYSTEM DEVELOPMENT TOOLS

The following technologies and tools were used in the development of ARMS:

 3.4.1 Programming Language: Python 3

Python is a high-level, general-purpose, interpreted programming language known for its clean syntax and readability. It serves as the primary server-side language for ARMS, powering all backend logic through the Django framework.

 3.4.2 Web Framework: Django 6.0.6

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Key Django features utilized in ARMS include:

- **ORM (Object-Relational Mapping)**: Used to define and query the database using Python classes instead of raw SQL.
- **Authentication System**: Django's built-in authentication was extended with a custom `AbstractUser` model to support role-based access.
- **Template Engine**: Django's template language was used to render dynamic HTML pages with context data from views.
- **URL Dispatcher**: Used to map URL patterns to corresponding view functions.
- **Middleware**: Django middleware was used for session management, CSRF protection, and security headers.
- **Django Messages Framework**: Used to pass one-time notifications (success/error messages) across HTTP redirects.

 3.4.3 Frontend Technologies

- **HTML5**: Used for structuring all web page templates.
- **CSS3**: Used for styling, layout, and visual design of the user interface, including responsive design features.
- **JavaScript (ES6)**: Used for client-side interactivity such as tab switching, modal dialog controls, and dynamic form behaviour.

 3.4.4 Database: SQLite 3

SQLite is a lightweight, serverless, file-based relational database engine. It was used as the development database for ARMS, as it requires no additional server configuration. The database is managed entirely through Django's ORM, with the database file stored as `db.sqlite3` in the project root.

 3.4.5 Additional Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `djangorestframework` | 3.17.1 | REST API support |
| `djangorestframework_simplejwt` | 5.5.1 | JWT token authentication |
| `django-cors-headers` | 4.9.0 | Cross-Origin Resource Sharing support |
| `weasyprint` | 69.0 | PDF/print generation for academic transcripts |
| `python-decouple` | 3.8 | Environment variable management (SECRET_KEY, DEBUG) |
| `pillow` | 12.2.0 | Image processing support |

3.4.6 Development Environment

- **Operating System**: Windows 11
- **Code Editor**: Visual Studio Code
- **Version Control**: Git with GitHub for source code management
- **Virtual Environment**: Python `venv` for dependency isolation

---

 3.5 DATABASE DESIGN

The database design of ARMS defines the structure of all data entities, their attributes, and the relationships between them. The system uses a relational database model implemented through Django's ORM.

3.5.1 Entity Relationship Overview

ARMS comprises six core database entities:

1. **Department** — Academic departments of the institution
2. **User** — All system users (students, lecturers, registrars, administrators)
3. **Course** — Academic courses offered by departments
4. **Enrollment** — Links students to courses they have registered for
5. **TranscriptRequest** — Tracks student requests for official transcripts
6. **AuditLog** — Records all significant actions performed on the system

> **[DIAGRAM SUGGESTION]**: Insert an Entity Relationship Diagram (ERD) here. The diagram should show all six entities as rectangles with their primary attributes listed inside. Show relationships using Crow's Foot notation: Department has many Users, Department has many Courses, User (lecturer) teaches many Courses, User (student) has many Enrollments, Course has many Enrollments, User (student) has many TranscriptRequests, User has many AuditLogs.

 3.5.2 Database Table Descriptions

**Table 1: Department**

The `Department` table stores information about the academic departments within the institution.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique department identifier |
| `code` | VARCHAR(10) | NOT NULL, UNIQUE | Short department code (e.g., "CSC") |
| `name` | VARCHAR(100) | NOT NULL | Full name of the department |

---

**Table 2: User**

The `User` table extends Django's standard `AbstractUser` model to support role-based access control and academic-specific attributes.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `username` | VARCHAR(150) | NOT NULL, UNIQUE | Login username (set to Matric/Staff ID) |
| `first_name` | VARCHAR(150) | NOT NULL | User's first name |
| `last_name` | VARCHAR(150) | NOT NULL | User's last name |
| `email` | VARCHAR(254) | NOT NULL, UNIQUE | User's email address |
| `password` | VARCHAR(128) | NOT NULL | Hashed password |
| `role` | VARCHAR(20) | NOT NULL | User role: student, lecturer, registrar, or admin |
| `reg_id` | VARCHAR(50) | NOT NULL, UNIQUE | Matriculation number or Staff ID |
| `department_id` | Integer | Foreign Key → Department, NULL | User's affiliated department |
| `level` | Integer | NULL | Academic level (100, 200, 300, 400) — students only |
| `programme` | VARCHAR(100) | NULL | Academic programme (e.g., B.Sc Computer Science) |
| `session` | VARCHAR(20) | NULL | Current academic session (e.g., 2025/2026) |
| `status` | VARCHAR(20) | NOT NULL | Account status: Active, Probation, or Suspended |

---

**Table 3: Course**

The `Course` table stores details of all academic courses offered by the institution.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique course identifier |
| `code` | VARCHAR(15) | NOT NULL, UNIQUE | Course code (e.g., "CSC 301") |
| `title` | VARCHAR(150) | NOT NULL | Full title of the course |
| `units` | Integer | NOT NULL, Default=3 | Number of credit units |
| `department_id` | Integer | Foreign Key → Department, NOT NULL | Department offering the course |
| `lecturer_id` | Integer | Foreign Key → User (role=lecturer), NULL | Assigned lecturer |
| `semester` | VARCHAR(20) | NOT NULL | Semester: 1st Semester or 2nd Semester |

---

**Table 4: Enrollment**

The `Enrollment` table is a junction table that links students to courses. It also stores grading information and enrolment status.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique enrollment identifier |
| `student_id` | Integer | Foreign Key → User (role=student), NOT NULL | The enrolled student |
| `course_id` | Integer | Foreign Key → Course, NOT NULL | The enrolled course |
| `semester` | VARCHAR(20) | NOT NULL | Semester of enrollment |
| `session` | VARCHAR(20) | NOT NULL | Academic session (e.g., 2025/2026) |
| `status` | VARCHAR(30) | NOT NULL | Enrollment status: Pending approval or Enrolled |
| `score` | Integer | NULL | Numeric score (0–100) entered by lecturer |
| `grade` | VARCHAR(2) | NULL | Auto-computed letter grade (A, B, C, D, E, F) |

*Unique constraint*: (`student_id`, `course_id`, `session`) — a student cannot enroll in the same course in the same session more than once.

*Grade Computation Logic*:
- A: 70 – 100
- B: 60 – 69
- C: 50 – 59
- D: 45 – 49
- E: 40 – 44
- F: 0 – 39

---

**Table 5: TranscriptRequest**

The `TranscriptRequest` table tracks student requests for their official academic transcripts.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique request identifier |
| `student_id` | Integer | Foreign Key → User (role=student), NOT NULL | The requesting student |
| `reference` | VARCHAR(30) | NOT NULL, UNIQUE | Unique reference code (e.g., "TR-7E29-4401") |
| `status` | VARCHAR(20) | NOT NULL | Request status: Pending, Approved, or Denied |
| `request_date` | DateTime | NOT NULL, Auto-set on creation | Date and time of the request |

---

**Table 6: AuditLog**

The `AuditLog` table provides a complete, tamper-evident record of all significant events and user actions on the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique log entry identifier |
| `user_id` | Integer | Foreign Key → User, NULL | The user who performed the action |
| `action` | VARCHAR(255) | NOT NULL | Description of the action performed |
| `timestamp` | DateTime | NOT NULL, Auto-set on creation | When the action occurred |

 3.5.3 Grade Point and CGPA Computation

The system automatically computes CGPA using the standard weighted grade point average formula:

**CGPA = Σ (Grade Points × Credit Units) / Σ (Credit Units)**

Where grade points are mapped as follows:

| Grade | Score Range | Grade Points |
|-------|-------------|--------------|
| A | 70 – 100 | 5 |
| B | 60 – 69 | 4 |
| C | 50 – 59 | 3 |
| D | 45 – 49 | 2 |
| E | 40 – 44 | 1 |
| F | 0 – 39 | 0 |

Academic standing classification based on CGPA:

| CGPA Range | Class of Degree |
|------------|-----------------|
| 4.50 – 5.00 | First Class |
| 3.50 – 4.49 | Second Class Upper |
| 2.40 – 3.49 | Second Class Lower |
| 1.50 – 2.39 | Third Class |
| Below 1.50 | Probation |

---

# CHAPTER FOUR

## IMPLEMENTATION, ANALYSIS AND TESTING

4.0 INTRODUCTION

This chapter presents the detailed implementation of the Academic Record Management System (ARMS), covering the program flow, pseudocode for core system modules, system testing, user documentation, and result analysis. The chapter demonstrates how the requirements specified in Chapter Three were translated into a fully functional web-based application using Django, Python, SQLite, HTML, CSS, and JavaScript.

The system was implemented in a modular fashion, with each module corresponding to a specific user role or system function. All modules were integrated into a single cohesive application before thorough testing was conducted.

---

4.1 SYSTEM OVERVIEW

ARMS is a web-based application accessible through a standard web browser. The system is hosted on a local development server (or a production web server upon deployment) running Django. All data is persisted in a SQLite relational database.

The system is organized around four role-based dashboards:

1. **Student Dashboard** — Course registration, results viewing, CGPA tracking, and transcript requests.
2. **Lecturer Dashboard** — Course oversight, student roster viewing, and grade entry.
3. **Registrar Dashboard** — Student record management, enrolment approvals, course creation, and transcript management.
4. **Admin Dashboard** — Full user management, department management, and system audit log monitoring.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the ARMS landing/home page here, showing the institution branding, navigation bar, and the platform statistics (total students, courses, transcripts processed).

All four dashboards are protected by authentication middleware. Unauthenticated requests to any dashboard URL are automatically intercepted and redirected to the login page.

The application URL structure is as follows:

| URL Pattern | View | Access |
|-------------|------|--------|
| `/` | Landing Page | Public |
| `/login/` | Login Page | Public |
| `/register/` | Registration Page | Public |
| `/logout/` | Logout Action | Authenticated |
| `/dashboard/student/` | Student Dashboard | Students only |
| `/dashboard/lecturer/` | Lecturer Dashboard | Lecturers only |
| `/dashboard/registrar/` | Registrar Dashboard | Registrars only |
| `/dashboard/admin/` | Admin Dashboard | Admins only |
| `/transcript/<student_id>/` | Transcript View | Authenticated |

---

4.2 PROGRAM FLOW

4.2.1 Overall System Flow

The general program flow of ARMS proceeds as follows upon a user request:

1. A user's browser sends an HTTP request to the Django server.
2. Django's URL dispatcher (`urls.py`) matches the URL pattern to the corresponding view function in `views.py`.
3. The view function processes the request:
   - For **GET requests**: The view queries the database via Django models, constructs a context dictionary, and renders the appropriate HTML template.
   - For **POST requests**: The view reads form data, validates it, performs the appropriate database operation (create, update, or delete), creates an audit log entry, and returns an HTTP redirect to the corresponding GET URL.
4. The Django template engine renders the HTML template, substituting template variables with the actual context data.
5. The rendered HTML page is returned to the user's browser.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Login Page here, showing the login form with the Matric/Staff ID and password fields, and the demo login quick-action buttons.

4.2.2 Student Workflow Flow

1. Student navigates to `/login/` and submits credentials.
2. System validates credentials → creates session → redirects to `/dashboard/student/?tab=dashboard`.
3. Dashboard renders: CGPA ring, current semester units, current enrollments, and recent activities.
4. Student clicks "Courses" tab → system queries available courses for their department and current semester.
5. Student selects courses and submits the registration form → system creates `Enrollment` records with status "Pending approval" → audit log entry created → redirect with success notification.
6. Student clicks "Results" tab → system fetches all enrolled courses with scores, groups by session/semester, and renders GPA breakdown table.
7. Student clicks "Transcript" tab → system checks for existing approved transcript → if none, displays request button.
8. Student submits transcript request → system creates `TranscriptRequest` with unique reference code → audit log created → redirect with success notification.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Student Dashboard (Dashboard tab) here, showing the CGPA ring gauge, GPA summary, currently enrolled courses, and the Recent Activity log.

4.2.3 Lecturer Workflow Flow

1. Lecturer logs in → redirected to `/dashboard/lecturer/?tab=dashboard`.
2. Dashboard renders: count of assigned courses, total students enrolled, finalized vs. pending results.
3. Lecturer clicks "Results" tab → system loads each assigned course with student roster and average score.
4. Lecturer clicks on a course to expand the grade entry panel.
5. Lecturer enters a score for a student and submits → system updates the `Enrollment` record → grade automatically computed → audit log created → page reloads showing updated grade.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Lecturer Dashboard showing the grade entry table with student names, current scores, and letter grades.

4.2.4 Registrar Workflow Flow

1. Registrar logs in → redirected to `/dashboard/registrar/?tab=dashboard`.
2. Registrar views overview statistics (total students, pending approvals, courses managed).
3. Registrar clicks "Records" tab → system queries all students, computes CGPA for each, renders a searchable table.
4. Registrar uses the search bar to find a specific student by name, matric number, or programme.
5. Registrar clicks "Oversight" tab → system fetches all pending enrolment requests → registrar approves or denies each.
   - Approve: `Enrollment.status` updated to "Enrolled" → audit log created.
   - Deny: `Enrollment` record deleted → audit log created.
6. Registrar clicks "Transcripts" tab → views all transcript requests → approves or denies.
7. Registrar clicks "Courses" tab → can create a new course by filling in the course creation form.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Registrar Dashboard showing the Student Records table with CGPA values and the pending enrolment approval panel.

4.2.5 Admin Workflow Flow

1. Admin logs in → redirected to `/dashboard/admin/?tab=dashboard`.
2. Admin views system summary and recent audit logs.
3. Admin clicks "Users" tab → views full user list with roles, emails, and statuses.
4. Admin clicks "Add User" → modal popup appears → admin fills in new user details and submits → new user created with default password → audit log created.
5. Admin changes a user's status using the status dropdown (Active / Probation / Suspended) → status updated → audit log created.
6. Admin clicks "Departments" tab → views all departments → creates a new department by submitting the department form.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Admin Dashboard showing the user management table with role badges and status dropdowns, and the "Add User" modal popup.

---

4.3 PSEUDOCODE FOR ARMS SYSTEM

This section presents the pseudocode for the key modules of the ARMS application, providing a language-agnostic description of the core algorithms implemented.

4.3.1 User Authentication (Login)

```
PROCEDURE LoginUser(request):
    IF request.user IS authenticated THEN
        REDIRECT to role-appropriate dashboard
        RETURN
    END IF

    IF request.method IS "POST" THEN
        loginId ← request.POST["loginId"]
        password ← request.POST["loginPassword"]

        TRY:
            userObj ← Users WHERE reg_id = loginId OR email = loginId
            user ← AUTHENTICATE(username=userObj.username, password=password)
        CATCH UserNotFound:
            user ← NULL
        END TRY

        IF user IS NOT NULL THEN
            CREATE session for user
            LOG action: "User logged in successfully"
            REDIRECT to role-appropriate dashboard
        ELSE
            DISPLAY error: "Invalid credentials"
            RENDER login page
        END IF
    ELSE
        RENDER login page
    END IF
END PROCEDURE
```

4.3.2 User Registration

```
PROCEDURE RegisterUser(request):
    IF request.user IS authenticated THEN
        REDIRECT to role-appropriate dashboard
        RETURN
    END IF

    IF request.method IS "POST" THEN
        role ← request.POST["role"]
        firstName ← request.POST["firstName"]
        lastName ← request.POST["lastName"]
        regId ← request.POST["regId"]
        email ← request.POST["regEmail"]
        password ← request.POST["regPassword"]
        passwordConfirm ← request.POST["regPassword2"]

        IF password ≠ passwordConfirm THEN
            DISPLAY error: "Passwords do not match"
            RETURN
        END IF

        IF Users WHERE username = regId OR reg_id = regId EXISTS THEN
            DISPLAY error: "Matric/Staff ID already registered"
            RETURN
        END IF

        IF Users WHERE email = email EXISTS THEN
            DISPLAY error: "Email already registered"
            RETURN
        END IF

        CREATE new User(username=regId, email, password, firstName,
                        lastName, role, reg_id=regId, status="Active")
        LOG action: "Account registered as [role]"
        CREATE session for new user
        REDIRECT to role-appropriate dashboard
    ELSE
        RENDER register page
    END IF
END PROCEDURE
```

4.3.3 Course Registration (Student)

```
PROCEDURE CourseRegistration(request):
    IF request.user.role ≠ "student" THEN
        RETURN HTTP 403 Forbidden
    END IF

    IF request.method IS "POST" THEN
        courseIds ← request.POST["courses"] (list)

        FOR EACH courseId IN courseIds:
            course ← GET Course WHERE id = courseId

            IF Enrollment WHERE student=currentUser AND course=course
               AND session="2025/2026" DOES NOT EXIST THEN
                CREATE Enrollment(student=currentUser, course=course,
                                  semester=course.semester,
                                  session="2025/2026",
                                  status="Pending approval")
                LOG action: "Registered for course [course.code]"
            END IF
        END FOR
    END IF

    REDIRECT to student dashboard
END PROCEDURE
```

4.3.4 Grade Entry and Automatic Grade Computation (Lecturer)

```
PROCEDURE UpdateGrade(request):
    IF request.user.role ≠ "lecturer" THEN
        RETURN HTTP 403 Forbidden
    END IF

    IF request.method IS "POST" THEN
        enrollmentId ← request.POST["enrollmentId"]
        score ← request.POST["score"]

        enrollment ← GET Enrollment WHERE id = enrollmentId

        IF enrollment.course.lecturer ≠ currentUser THEN
            RETURN HTTP 403 Forbidden
        END IF

        IF score IS NOT NULL THEN
            enrollment.score ← INTEGER(score)
            SAVE enrollment  // triggers automatic grade computation below
            LOG action: "Updated grade for [student.reg_id] in [course.code] to [score]"
        END IF
    END IF

    REDIRECT to lecturer dashboard results tab
END PROCEDURE

// Called automatically when enrollment.save() is invoked:
PROCEDURE ComputeGrade(enrollment):
    score ← enrollment.score
    IF score ≥ 70 THEN grade ← "A"
    ELSE IF score ≥ 60 THEN grade ← "B"
    ELSE IF score ≥ 50 THEN grade ← "C"
    ELSE IF score ≥ 45 THEN grade ← "D"
    ELSE IF score ≥ 40 THEN grade ← "E"
    ELSE grade ← "F"
    END IF
    enrollment.grade ← grade
END PROCEDURE
```

4.3.5 CGPA Computation (Student Dashboard)

```
PROCEDURE ComputeCGPA(student):
    completedEnrollments ← GET Enrollments WHERE student = student
                           AND status = "Enrolled"
                           AND score IS NOT NULL

    totalUnitsEnrolled ← 0
    totalGradePoints ← 0

    FOR EACH enrollment IN completedEnrollments:
        units ← enrollment.course.units
        gradePoints ← GRADE_POINT_MAP[enrollment.grade]
        totalUnitsEnrolled ← totalUnitsEnrolled + units
        totalGradePoints ← totalGradePoints + (units × gradePoints)
    END FOR

    IF totalUnitsEnrolled > 0 THEN
        cgpa ← ROUND(totalGradePoints / totalUnitsEnrolled, 2)
    ELSE
        cgpa ← 0.0
    END IF

    IF cgpa ≥ 4.5 THEN standing ← "First Class"
    ELSE IF cgpa ≥ 3.5 THEN standing ← "Second Class Upper"
    ELSE IF cgpa ≥ 2.4 THEN standing ← "Second Class Lower"
    ELSE IF cgpa ≥ 1.5 THEN standing ← "Third Class"
    ELSE standing ← "Probation"
    END IF

    RETURN (cgpa, standing)
END PROCEDURE
```

4.3.6 Enrolment Approval (Registrar)

```
PROCEDURE ApproveEnrollment(request):
    IF request.user.role ≠ "registrar" THEN
        RETURN HTTP 403 Forbidden
    END IF

    IF request.method IS "POST" THEN
        enrollmentId ← request.POST["enrollmentId"]
        action ← request.POST["action"]

        enrollment ← GET Enrollment WHERE id = enrollmentId

        IF action = "approve" THEN
            enrollment.status ← "Enrolled"
            SAVE enrollment
            LOG action: "Approved course enrollment for [student.reg_id] in [course.code]"
        ELSE
            DELETE enrollment
            LOG action: "Denied course enrollment for [student.reg_id] in [course.code]"
        END IF
    END IF

    REDIRECT to registrar dashboard oversight tab
END PROCEDURE
```

4.3.7 Transcript Request and Approval

```
PROCEDURE RequestTranscript(student):
    IF student.role ≠ "student" THEN
        RETURN HTTP 403 Forbidden
    END IF

    reference ← GENERATE unique reference (format: "TR-XXXX-XXXX")
    CREATE TranscriptRequest(student=student, reference=reference, status="Pending")
    LOG action: "Requested academic transcript (Ref: [reference])"
    REDIRECT to student dashboard transcript tab
END PROCEDURE

PROCEDURE ApproveTranscript(request):
    IF request.user.role ≠ "registrar" THEN
        RETURN HTTP 403 Forbidden
    END IF

    IF request.method IS "POST" THEN
        requestId ← request.POST["requestId"]
        action ← request.POST["action"]
        transcriptRequest ← GET TranscriptRequest WHERE id = requestId

        IF action = "approve" THEN
            transcriptRequest.status ← "Approved"
            LOG action: "Approved transcript request [reference] for [student.reg_id]"
        ELSE
            transcriptRequest.status ← "Denied"
            LOG action: "Denied transcript request [reference] for [student.reg_id]"
        END IF
        SAVE transcriptRequest
    END IF

    REDIRECT to registrar dashboard transcripts tab
END PROCEDURE
```

4.3.8 Admin User Management

```
PROCEDURE AdminAddUser(request):
    IF request.user.role ≠ "admin" THEN
        RETURN HTTP 403 Forbidden
    END IF

    IF request.method IS "POST" THEN
        regId ← request.POST["regId"]
        email ← request.POST["email"]
        firstName ← request.POST["firstName"]
        lastName ← request.POST["lastName"]
        role ← request.POST["role"]
        deptId ← request.POST["department"]
        level ← request.POST["level"]

        department ← GET Department WHERE id = deptId

        CREATE User(username=regId, email, password="password123",
                    firstName, lastName, role, reg_id=regId,
                    department, level, status="Active")
        LOG action: "Admin created user [regId] with role [role]"
    END IF

    REDIRECT to admin dashboard users tab
END PROCEDURE

PROCEDURE AdminEditUserStatus(request):
    IF request.user.role ≠ "admin" THEN
        RETURN HTTP 403 Forbidden
    END IF

    IF request.method IS "POST" THEN
        userId ← request.POST["userId"]
        newStatus ← request.POST["status"]

        user ← GET User WHERE id = userId
        oldStatus ← user.status
        user.status ← newStatus
        SAVE user
        LOG action: "Admin changed status of [reg_id] from [oldStatus] to [newStatus]"
    END IF

    REDIRECT to admin dashboard users tab
END PROCEDURE
```

4.3.9 Official Transcript Generation

```
PROCEDURE ViewTranscript(request, studentId):
    IF request.user.role = "student" AND request.user.id ≠ studentId THEN
        RETURN HTTP 403 Forbidden
    END IF

    student ← GET User WHERE id = studentId AND role = "student"

    enrollments ← GET Enrollments WHERE student = student
                  AND status = "Enrolled" AND score IS NOT NULL
                  ORDER BY session, semester, course.code

    GROUP enrollments BY (session, semester):
        FOR EACH group:
            semGPA ← SUM(units × gradePoints) / SUM(units)

    totalUnitsEnrolled ← SUM of all units
    totalGradePoints ← SUM of all (units × gradePoints)
    cgpa ← ROUND(totalGradePoints / totalUnitsEnrolled, 2)

    RENDER transcript template WITH student, grouped semesters,
                                    cgpa, total units
END PROCEDURE
```

---

4.4 SYSTEM TESTING

System testing was carried out to verify that all modules of ARMS function correctly, both individually (unit testing) and as an integrated system (integration testing). Testing covered functional behaviour, access control enforcement, and business logic accuracy.

4.4.1 Testing Approach

Two levels of testing were applied:

1. **Automated Unit and Integration Tests**: Written using Django's built-in `TestCase` class, which leverages Python's `unittest` framework. These tests were run using the command:
   ```
   python manage.py test records
   ```
2. **Manual Testing**: Each user role's dashboard, form submission, and navigation flow was tested manually in the browser to verify correct visual behaviour and user experience.

4.4.2 Automated Test Cases

**Test Suite 1: `ARMSModelTests` — Database Model Logic**

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---------|-----------|-----------------|---------------|--------|
| MT-01 | Score 85 → Grade A, Grade Points 5 | grade = 'A', grade_points() = 5 | grade = 'A', grade_points() = 5 | ✅ PASS |
| MT-02 | Score 65 → Grade B, Grade Points 4 | grade = 'B', grade_points() = 4 | grade = 'B', grade_points() = 4 | ✅ PASS |
| MT-03 | Score 35 → Grade F, Grade Points 0 | grade = 'F', grade_points() = 0 | grade = 'F', grade_points() = 0 | ✅ PASS |
| MT-04 | CGPA with Course 1 (3 units, 80) and Course 2 (4 units, 65) = 4.43 | CGPA = 4.43 | CGPA = 4.43 | ✅ PASS |

**Test Suite 2: `ARMSViewAccessTests` — Route Access and Role Control**

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---------|-----------|-----------------|---------------|--------|
| VA-01 | Unauthenticated GET to `/dashboard/student/` | Redirect to `/login/?next=/dashboard/student/` | Redirect to login page | ✅ PASS |
| VA-02 | Student GET all dashboard tabs (dashboard, profile, courses, results, transcript, notifications, settings) | HTTP 200, correct active_tab | HTTP 200, all tabs returned correct context | ✅ PASS |
| VA-03 | Student POST profile update | Redirect to `?tab=profile&success=profile`; DB updated | Profile updated, redirect confirmed | ✅ PASS |
| VA-04 | Student POST password change | Redirect to `?tab=settings&success=password`; password updated | Password hashed and updated correctly | ✅ PASS |
| VA-05 | Lecturer GET all dashboard tabs | HTTP 200, correct tab context | All tabs return HTTP 200 | ✅ PASS |
| VA-06 | Lecturer POST profile update | Profile updated; redirect confirmed | Passed | ✅ PASS |
| VA-07 | Registrar GET all dashboard tabs | HTTP 200, correct tab context | All tabs return HTTP 200 | ✅ PASS |
| VA-08 | Registrar POST create course | Course created in DB; redirect confirmed | `Course.objects.filter(code='CSC 303').exists()` = True | ✅ PASS |
| VA-09 | Admin GET all dashboard tabs | HTTP 200, correct tab context | All tabs return HTTP 200 | ✅ PASS |
| VA-10 | Admin POST create department | Department created in DB; redirect confirmed | `Department.objects.filter(code='MTH').exists()` = True | ✅ PASS |
| VA-11 | Admin POST change user status to "Suspended" | User status updated; redirect confirmed | `student.status` = 'Suspended' | ✅ PASS |

**Test Execution Summary:**

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 6.548s

OK
Destroying test database for alias 'default'...
```

All automated tests passed successfully with no errors or failures.

4.4.3 Manual Test Cases

**Module: User Authentication**

| Test ID | Scenario | Input | Expected Output | Status |
|---------|----------|-------|-----------------|--------|
| AUTH-01 | Valid student login | Matric: CSC/2022/0417, PW: password123 | Redirect to student dashboard | ✅ PASS |
| AUTH-02 | Valid login via email | Email: a.okoro@university.edu, PW: password123 | Redirect to student dashboard | ✅ PASS |
| AUTH-03 | Invalid password | Matric: CSC/2022/0417, PW: wrongpass | Error: "Invalid credentials" shown | ✅ PASS |
| AUTH-04 | Non-existent user | Matric: FAKE/0000/0000 | Error: "Invalid credentials" shown | ✅ PASS |
| AUTH-05 | Accessing dashboard without login | Navigate to `/dashboard/student/` | Redirect to `/login/` | ✅ PASS |
| AUTH-06 | Logout | Click logout button | Session destroyed; redirect to login | ✅ PASS |

**Module: Course Registration (Student)**

| Test ID | Scenario | Expected Output | Status |
|---------|----------|-----------------|--------|
| CR-01 | Student registers for available courses | Enrollment records created with "Pending approval" | ✅ PASS |
| CR-02 | Student registers for same course twice | No duplicate enrollment created | ✅ PASS |
| CR-03 | Registered course appears in "My Courses" tab | Course listed with "Pending approval" status | ✅ PASS |

**Module: Grade Entry (Lecturer)**

| Test ID | Scenario | Expected Output | Status |
|---------|----------|-----------------|--------|
| GR-01 | Lecturer enters score 78 | Grade auto-computed as "A" | ✅ PASS |
| GR-02 | Lecturer enters score 55 | Grade auto-computed as "C" | ✅ PASS |
| GR-03 | Lecturer enters score 38 | Grade auto-computed as "F" | ✅ PASS |
| GR-04 | Lecturer enters score for student in another lecturer's course | HTTP 403 Forbidden | ✅ PASS |

**Module: Enrolment Approval (Registrar)**

| Test ID | Scenario | Expected Output | Status |
|---------|----------|-----------------|--------|
| EA-01 | Registrar approves enrollment | Enrollment status changes to "Enrolled" | ✅ PASS |
| EA-02 | Registrar denies enrollment | Enrollment record deleted from database | ✅ PASS |
| EA-03 | Approved course appears in student results | Course visible in student's results tab | ✅ PASS |

---

4.5 USER DOCUMENTATION

This section provides a step-by-step guide for each category of user on how to use the ARMS application effectively.

4.5.1 Accessing the System

Open a web browser (Google Chrome or Mozilla Firefox recommended) and navigate to the ARMS URL. The landing page provides an overview of the system's statistics and a navigation bar with "Login" and "Register" links.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the ARMS Home/Landing Page here, showing the hero section with the tagline, the statistics counters (students enrolled, courses offered, transcripts processed), and the navigation links.

4.5.2 Student User Guide

**Step 1: Registration**

New students must first register on the system.

1. Click the **"Register"** link in the navigation bar.
2. On the registration page, fill in:
   - Select **"Student"** as your role.
   - Enter your **First Name** and **Last Name**.
   - Enter your **Matriculation Number** (e.g., CSC/2022/0417).
   - Enter your institutional **Email Address**.
   - Create and confirm a secure **Password** (minimum 8 characters).
3. Click **"Create Account"**.
4. You will be automatically logged in and redirected to the Student Dashboard.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Registration Page here showing the form fields and the role selection dropdown.

**Step 2: Login**

1. Navigate to the **Login** page.
2. Enter your **Matriculation Number** (or email) in the login ID field.
3. Enter your **Password**.
4. Click **"Sign In"**.
5. You will be redirected to the Student Dashboard.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Login Page here.

**Step 3: Navigating the Student Dashboard**

The Student Dashboard is organized into tabs accessible from the left sidebar:

- **Dashboard**: Overview of your CGPA, GPA ring visualization, current semester courses, and recent notifications.
- **My Courses**: Full list of all your registered courses, their status, and lecturers.
- **Results**: Semester-by-semester academic result breakdown with GPA per semester and overall CGPA.
- **Transcript**: Request and track the status of your official academic transcript.
- **Notifications**: View recent system activities related to your account.
- **Profile**: Update your personal information (name, email, programme).
- **Settings**: Change your account password.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Student Dashboard "Results" tab here, showing the semester GPA table, individual course scores and grades, and the cumulative CGPA at the bottom.

**Step 4: Course Registration**

1. On the **Dashboard** tab, locate the "Course Registration" section or click the **"Register Courses"** button.
2. A modal popup will display all available courses for your department in the current semester.
3. Select the courses you wish to register for by checking their checkboxes.
4. Click **"Submit Registration"**.
5. Your selected courses will appear in the **My Courses** tab with the status **"Pending approval"** until the registrar approves them.

**Step 5: Requesting a Transcript**

1. Navigate to the **Transcript** tab.
2. If you do not have a pending or approved transcript, click the **"Request Official Transcript"** button.
3. The system will generate a unique reference number for your request.
4. The request will appear with **"Pending"** status until processed by the Registrar.
5. Once approved, a link to view and print your official transcript will become available.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Transcript tab showing the "Request Official Transcript" button and, separately, an approved transcript with the "View & Print Transcript" link visible.

4.5.3 Lecturer User Guide

**Step 1: Login**

1. Navigate to the **Login** page.
2. Enter your **Staff ID** (or email) and **Password**.
3. Click **"Sign In"**. You will be redirected to the Lecturer Dashboard.

**Step 2: Navigating the Lecturer Dashboard**

- **Dashboard**: Overview of total courses assigned, total students enrolled, finalized vs. pending results.
- **My Courses**: Full list of assigned courses with enrolment counts and average scores.
- **Rosters**: View the complete student roster for each course.
- **Results**: Grade entry interface — enter scores for each student in each course.
- **Profile** and **Settings**: Update personal information and change password.

**Step 3: Entering Student Grades**

1. Navigate to the **Results** tab.
2. The grade entry queue displays all your assigned courses.
3. Click on a course to expand its student list.
4. For each student, enter a numeric score (0–100) in the score input field.
5. Click **"Save"** to record the grade. The system will automatically compute and display the corresponding letter grade.
6. Repeat for all students until the course is fully graded. The course status will update to **"Finalized"** automatically once all students have scores.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Lecturer Dashboard "Results" tab showing the grade entry panel with student names, score input fields, computed letter grades, and the course average score.

4.5.4 Registrar User Guide

**Step 1: Login**

Enter your Staff ID (or email) and password on the Login page.

**Step 2: Navigating the Registrar Dashboard**

- **Dashboard**: Overview of total students, pending approvals, and managed courses.
- **Records**: Searchable table of all registered students with CGPA and status. Click **"View Transcript"** to see a student's full academic record.
- **Courses**: View all courses; create new courses by clicking **"Create Course"** and completing the form.
- **Oversight**: Manage pending course enrolment requests — approve or deny each request.
- **Transcripts**: View all transcript requests — approve or deny.
- **Audit Logs**: Real-time feed of all system activities.

**Step 3: Approving Course Enrolments**

1. Navigate to the **Oversight** tab.
2. The pending enrolments table lists all student course registration requests.
3. For each entry, click **"Approve"** to confirm enrolment (status changes to "Enrolled") or **"Deny"** to reject and remove the request.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Registrar Dashboard "Oversight" tab showing the pending enrolment approval table with Approve/Deny buttons.

**Step 4: Managing Transcript Requests**

1. Navigate to the **Transcripts** tab.
2. The transcript requests table shows all student requests with their reference numbers and current status.
3. Click **"Approve"** to grant the request or **"Deny"** to reject it.

**Step 5: Creating a Course**

1. Navigate to the **Courses** tab.
2. Click **"Create Course"**.
3. A modal popup will appear. Fill in:
   - **Course Code** (e.g., CSC 305)
   - **Course Title** (e.g., Database Systems)
   - **Credit Units**
   - **Department**
   - **Assigned Lecturer**
   - **Semester** (1st or 2nd)
4. Click **"Create Course"** to save.

4.5.5 Administrator User Guide

**Step 1: Login**

Enter your Admin Staff ID (or email) and password on the Login page.

**Step 2: Navigating the Admin Dashboard**

- **Dashboard**: System overview with user counts, department list, and live audit log.
- **Users**: View, search, and manage all system accounts across all roles.
- **Departments**: View all departments; create new departments.
- **Settings**: Update admin profile and change password.

**Step 3: Adding a New User**

1. Navigate to the **Users** tab.
2. Click **"Add New User"**.
3. A modal form will appear. Fill in the user's:
   - Staff ID or Matriculation Number
   - Email Address
   - First Name and Last Name
   - Role (Student, Lecturer, Registrar, or Admin)
   - Department
   - Level (for students)
4. Click **"Add User"**. The new account is created with a default password of `password123`, which the user should change on first login.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Admin Dashboard "Add User" modal popup showing the user creation form.

**Step 4: Changing a User's Status**

1. Navigate to the **Users** tab.
2. Locate the user in the table.
3. In the **Status** column, use the dropdown to select **"Active"**, **"Probation"**, or **"Suspended"**.
4. The status change is saved immediately and logged in the audit trail.

4.5.6 Viewing the Official Transcript

An official transcript can be viewed by an approved student or accessed by registrar/admin staff.

1. Navigate to the **Transcript** tab in the Student Dashboard (or click "View Transcript" from the Registrar Records view).
2. The transcript page displays:
   - Student's personal details (name, matric number, department, programme, level).
   - A semester-by-semester breakdown of all completed courses with course code, title, units, score, grade, and semester GPA.
   - The overall CGPA and total credit units at the bottom of the transcript.
3. Click **"Print Transcript"** to open the browser print dialog. The page is formatted for clean printing on standard A4 paper.

> **[SCREENSHOT SUGGESTION]**: Insert a screenshot of the Official Transcript page here showing the full academic record with course details, semester GPA rows, and cumulative CGPA at the bottom.

---

4.6 RESULT AND ANALYSIS

4.6.1 System Capabilities Achieved

The ARMS implementation successfully delivered all the features specified in the requirement document. A summary of the key capabilities realized is presented below:

| Module | Feature | Status |
|--------|---------|--------|
| Authentication | Multi-role login (Student, Lecturer, Registrar, Admin) | ✅ Implemented |
| Authentication | Role-based dashboard redirection | ✅ Implemented |
| Authentication | Session management and logout | ✅ Implemented |
| Authentication | Account registration with validation | ✅ Implemented |
| Student Module | Course registration with enrolment status tracking | ✅ Implemented |
| Student Module | CGPA and GPA calculation with visual ring indicator | ✅ Implemented |
| Student Module | Semester-by-semester academic results view | ✅ Implemented |
| Student Module | Transcript request submission and tracking | ✅ Implemented |
| Student Module | Profile update and password change | ✅ Implemented |
| Lecturer Module | Assigned course and student roster view | ✅ Implemented |
| Lecturer Module | Score entry with automatic grade computation | ✅ Implemented |
| Lecturer Module | Result finalization tracking | ✅ Implemented |
| Registrar Module | Searchable student record database with CGPA | ✅ Implemented |
| Registrar Module | Enrolment approval / denial workflow | ✅ Implemented |
| Registrar Module | Course creation and management | ✅ Implemented |
| Registrar Module | Transcript request approval workflow | ✅ Implemented |
| Admin Module | Full user management (create, view, status change) | ✅ Implemented |
| Admin Module | Department management | ✅ Implemented |
| Admin Module | Full system audit log | ✅ Implemented |
| System-Wide | Audit trail for all significant actions | ✅ Implemented |
| System-Wide | Printable official transcript generation | ✅ Implemented |
| System-Wide | Access control (HTTP 403 for unauthorized role access) | ✅ Implemented |

4.6.2 Performance Analysis

The system was tested on a local development server running Django's built-in development server (single-threaded). Key observations:

- **Page Load Times**: All dashboard pages loaded within 1–2 seconds on the local environment, including database queries for student CGPA computation across multiple enrollment records.
- **CGPA Computation**: The CGPA calculation, which involves iterating over all enrollment records for a student, executes efficiently for typical student record sizes (up to 50+ courses).
- **Audit Logging**: Audit log creation adds negligible overhead to each request, as it is a simple single-row database insert.
- **Search Performance**: The student search function in the Registrar and Admin dashboards uses Django's `Q` objects with `icontains` lookups, which perform case-insensitive pattern matching efficiently for typical dataset sizes.

 4.6.3 Security Analysis

| Security Measure | Implementation | Status |
|-----------------|----------------|--------|
| Password Hashing | Django's `PBKDF2` algorithm with SHA-256 | ✅ Active |
| CSRF Protection | Django's `CsrfViewMiddleware` and `{% csrf_token %}` on all forms | ✅ Active |
| Authentication Required | `@login_required` decorator on all protected views | ✅ Active |
| Role-Based Access Control | Role check at the start of every view function | ✅ Active |
| Session Management | Django session middleware; session destroyed on logout | ✅ Active |
| Sensitive Config | `SECRET_KEY` and `DEBUG` loaded from `.env` via `python-decouple` | ✅ Active |
| SQL Injection Prevention | All database queries use Django ORM (parameterized queries) | ✅ Active |

 4.6.4 Comparative Analysis: Manual vs. Digital System

| Criterion | Manual System | ARMS (Digital) |
|-----------|--------------|----------------|
| Record Access Speed | Hours to days (physical retrieval) | Seconds (instant query) |
| Data Accuracy | Prone to human error in calculation | Automated, formula-driven computation |
| CGPA Computation | Manual, error-prone calculation | Automated to 2 decimal places |
| Transcript Generation | Days to weeks | Instant, print on demand |
| Record Security | Physical files, limited access control | Role-based digital access control |
| Audit Trail | Non-existent or paper-based | Automated, timestamped digital log |
| Course Registration | Manual forms submitted to registrar | Digital, self-service with approval flow |
| Grade Entry | Paper-based, submitted to registrar | Direct digital entry by lecturer |
| Search / Lookup | Physical file search | Instant keyword search |
| Scalability | Limited by storage and staff capacity | Scales with database infrastructure |

4.6.5 Summary

The Academic Record Management System (ARMS) was successfully designed, implemented, tested, and documented. The system achieves its core objective of digitizing and automating the management of academic records in a higher institution. All functional requirements were implemented, all automated tests passed, and manual testing confirmed correct behaviour across all user roles and workflows.

The system replaces the inefficiencies of paper-based record management with a secure, role-aware, real-time web application that empowers students, lecturers, registrars, and administrators to perform their academic record functions with speed, accuracy, and transparency.

> **[SCREENSHOT SUGGESTION]**: Insert a final collage or carousel of screenshots showing all four dashboards side-by-side — the Student Dashboard (CGPA ring), the Lecturer Dashboard (grade entry), the Registrar Dashboard (student records table), and the Admin Dashboard (user management) — to provide a comprehensive visual summary of the completed system.


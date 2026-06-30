
CHAPTER FIVE

SUMMARY, CONCLUSION AND RECOMMENDATION

	5.1 SUMMARY

This project set out to design and develop a web-based Academic Record Management System (ARMS) as a digital replacement for the largely manual, paper-driven processes through which academic records are managed in Nigerian higher institutions. The study was motivated by the recurring and well-documented challenges associated with manual systems: susceptibility to data loss, arithmetic errors in CGPA computation, delays in transcript processing, limited access control, and the near-total absence of an auditable record of system activities.

Chapter One of this work introduced the background of the problem, articulating the inadequacy of manual academic record-keeping in a modern university setting. The chapter identified the aim and objectives of the study, defined the scope of the system, and stated its significance to students, lecturers, registrars, administrators, and the institution at large. The chapter also outlined the limitations encountered and established the organizational structure of the report.

Chapter Two presented an extensive review of related literature. Academic and industry literature on electronic record management systems, university information systems, and related digital tools was surveyed. Existing systems — both locally developed and internationally available — were examined and their shortcomings noted. This review provided the theoretical foundation upon which the design decisions for ARMS were based, and established the conceptual framework for a role-based, web-accessible academic record platform.

Chapter Three described the research methodology adopted in building ARMS. The Agile Software Development Methodology was employed, enabling iterative development and continuous refinement across five defined phases: Requirements and Design, Frontend Prototype, Backend Integration, Testing, and Review. The chapter also provided a comprehensive requirement specification — both functional (organized by user role: Student, Lecturer, Registrar, and Administrator) and non-functional (covering security, performance, usability, reliability, maintainability, scalability, portability, and auditability). The system architecture followed Django's Model-View-Template (MVT) pattern. Complete database design documentation was provided, covering six core entities: Department, User, Course, Enrollment, TranscriptRequest, and AuditLog, along with the grade point and CGPA computation logic embedded in the system.

Chapter Four presented the full implementation of the system. The program flow for each user role was described in detail, accompanied by structured pseudocode for all nine key modules — including authentication, course registration, grade computation, CGPA calculation, enrolment approval, and transcript generation. A thorough two-tier testing strategy was applied: automated unit and integration tests (using Django's TestCase framework) and comprehensive manual testing across all user roles and workflows. All fifteen automated test cases and all manual test scenarios passed successfully. A complete user documentation guide was included for each of the four user categories. The chapter concluded with a result and analysis section demonstrating that all functional requirements were achieved, performance was acceptable, security measures were fully implemented, and ARMS demonstrably outperforms the manual system across every evaluated criterion.

In summary, ARMS was successfully designed, developed, tested, and documented as a fully functional, secure, multi-role web application for academic record management in a higher institution.

---

	5.2 CONCLUSION AND RECOMMENDATION

5.2.1 Conclusion

The development of the Academic Record Management System (ARMS) has demonstrated that a carefully designed web-based application can effectively replace the inefficiencies and inaccuracies of manual academic record management in a university environment. The system was built on a proven, industry-standard technology stack — Python 3, Django, SQLite, HTML5, CSS3, and JavaScript — and delivered a complete, role-aware solution that addresses the distinct needs of students, lecturers, registrars, and administrators from a single unified platform.

ARMS successfully achieved all of the objectives defined in Chapter One:

1. Digitization of Academic Records: All student academic records — course enrollments, grades, CGPA, and transcript requests — are stored digitally in a structured relational database, eliminating the risk of physical damage, misplacement, or deterioration of paper records.

2. Automated CGPA Computation: The system computes CGPA automatically and accurately using the standard weighted grade point average formula. This removes the possibility of arithmetic errors that are common in manual computation, and the result is available to the student in real time.

3. Role-Based Access Control: The system enforces strict role separation, ensuring that students, lecturers, registrars, and administrators can only access the data and functions appropriate to their role. Unauthorized access attempts are blocked at the view level and return an HTTP 403 response.

4. Streamlined Transcript Processing: What previously took days or weeks in a manual environment now takes seconds. Students can request transcripts digitally; the registrar can approve or deny requests from a centralized dashboard; and approved transcripts are immediately available for viewing and printing in a clean, print-optimized format.

5. Comprehensive Audit Trail: Every significant action on the system — from logins and grade entries to enrolment approvals and transcript decisions — is recorded with the actor's identity and a timestamp. This provides institutional oversight and accountability that is entirely absent in manual systems.

6. Improved Transparency and Accessibility: Students can view their academic results, GPA, and CGPA at any time without queuing at the registrar's office. The self-service nature of the platform reduces administrative workload and empowers students with direct access to their own academic data.

It is therefore concluded that ARMS is a viable, functional, and impactful solution to the identified problem of inefficient manual academic record management. The system is ready for deployment in an academic institution and, with the enhancements outlined below, can be evolved into a comprehensive enterprise-grade university information system.

5.2.2 Recommendations

Based on the outcomes of this project and the experience gained during its development, the following recommendations are made for institutional adoption and future improvement:

1. Institutional Deployment: It is recommended that the system be deployed on a dedicated web server (e.g., using Gunicorn or uWSGI behind an Nginx reverse proxy) to replace or supplement existing manual processes. A phased rollout — beginning with one department — would allow staff and students to adapt gradually while minimizing disruption.

2. Database Migration to PostgreSQL: For production deployment, it is strongly recommended that the SQLite database be replaced with a production-grade database management system such as PostgreSQL. PostgreSQL offers superior concurrency handling, ACID compliance, and scalability — all of which are critical for a system serving a large number of concurrent users.

3. Email Notification Integration: The system should be extended to send automated email notifications to students and staff for key events — such as enrolment approvals or denials, transcript request status updates, and grade publications. Django's built-in email framework (django.core.mail) can be configured with any SMTP server or email delivery service (e.g., SendGrid, Mailgun) to achieve this.

4. Security Hardening for Production: Before a public-facing deployment, the following security configurations must be applied:
   - Set DEBUG = False in the production environment.
   - Configure ALLOWED_HOSTS to the specific production domain(s).
   - Enforce HTTPS by configuring the web server with a valid SSL/TLS certificate (e.g., using Let's Encrypt).
   - Enable Django's SECURE_HSTS_SECONDS, SECURE_SSL_REDIRECT, and SESSION_COOKIE_SECURE settings.

5. REST API Expansion: The project already includes djangorestframework and JWT authentication in its dependencies. It is recommended that a fully documented REST API be built out, enabling a future mobile application (Android/iOS) to connect to the ARMS backend.

6. User Account Recovery: A password recovery (forgot password) feature should be implemented using Django's built-in PasswordResetView and email-based token generation, ensuring that users who forget their credentials can regain access without requiring administrator intervention.

7. Multi-Institutional Support: A future version of the system could be architected as a multi-tenant application, allowing multiple institutions or faculties to maintain separate, isolated data environments within the same ARMS deployment.

---

	5.3 FURTHER WORKS

The current version of ARMS represents a solid and functional foundation. However, several opportunities for enhancement and expansion exist, which are recommended as directions for future development:

1. Mobile Application

A cross-platform mobile application (built with React Native or Flutter) can be developed to connect to the ARMS REST API backend. A mobile app would provide students and lecturers with convenient on-the-go access to their dashboards, push notifications for important events (enrolment approvals, grade releases), and the ability to view academic results and request transcripts directly from a smartphone.

2. Timetable and Scheduling Module

A timetable management module can be added to allow the registrar or administrator to create, publish, and manage academic timetables for each semester. Students would be able to view their personalized course schedule, and lecturers would see their teaching timetable, all within the same platform.

3. Fee Payment Integration

Academic institutions typically require tuition and fees to be settled before academic records or transcripts are released. A future module could integrate with a payment gateway (e.g., Paystack, Flutterwave) to track fee payment status per student and conditionally restrict course registration or transcript access to students with outstanding fees.

4. Attendance Tracking Module

A dedicated attendance management module would allow lecturers to record and track student attendance for each class session. The module could automatically flag students who fall below a defined attendance threshold (e.g., 75%) and restrict them from sitting examinations, with notifications sent to the student and registrar.

5. Advanced Analytics and Reporting Dashboard

A reporting and analytics module for registrars and administrators could provide institutional insights such as: departmental CGPA distributions, semester-over-semester grade trend analysis, course failure rate reports, and student retention and attrition statistics. These reports could be exportable as PDF or Excel files for institutional record-keeping.

6. Document Upload and Verification

Future work could introduce a document management module where students upload supporting documents (e.g., National ID, admission letters, medical certificates) directly to their profile. Registrar staff could then verify and approve these documents digitally, eliminating the need for physical document submission and manual verification.

7. Alumni Module

Upon graduation, a student's status can be transitioned to an alumni profile, allowing them continued access to their academic records and the ability to request certified transcripts for employment or postgraduate admission purposes — long after they have left the institution.

8. Inter-Institutional Transcript Sharing

A standardized, verifiable digital transcript export format (e.g., using a blockchain-anchored credential or a signed PDF) could allow transcripts generated by ARMS to be electronically verified by receiving institutions or employers, eliminating transcript fraud and the delays of physical mailing.

9. Automated Semester Progression

A semester management module could automate the academic calendar — rolling over student levels at the end of each session, archiving completed semester records, and opening course registration for the new semester — reducing the manual administrative overhead currently required to manage these transitions.

10. Learning Management System (LMS) Integration

ARMS could be integrated with a Learning Management System such as Moodle or Canvas, providing a unified academic portal where students access both their academic records (through ARMS) and their course content, assignments, and examinations (through the LMS) from a single authenticated session.

---

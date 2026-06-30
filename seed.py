import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from records.models import Department, Course, Enrollment, TranscriptRequest, AuditLog
from datetime import datetime, timedelta

User = get_user_model()

def run():
    print("Seeding database...")
    # Clear existing data
    Enrollment.objects.all().delete()
    Course.objects.all().delete()
    TranscriptRequest.objects.all().delete()
    AuditLog.objects.all().delete()
    User.objects.all().delete()
    Department.objects.all().delete()

    # 1. Create Departments
    csc = Department.objects.create(code="CSC", name="Computer Science")
    eco = Department.objects.create(code="ECO", name="Economics")
    phy = Department.objects.create(code="PHY", name="Physics")
    law = Department.objects.create(code="LAW", name="Law")
    ict = Department.objects.create(code="ICT", name="ICT Directorate")
    acad = Department.objects.create(code="ACA", name="Academic Affairs")

    # 2. Create Users
    # Student
    adaeze = User.objects.create_user(
        username="CSC/2022/0417",
        email="a.okoro@university.edu",
        password="password123",
        first_name="Adaeze",
        last_name="Okoro",
        role="student",
        reg_id="CSC/2022/0417",
        department=csc,
        level=300,
        programme="B.Sc Computer Science",
        session="2025/2026",
        status="Active"
    )

    # Student 2 (for registrar list)
    chiamaka = User.objects.create_user(
        username="ECO/2021/0982",
        email="c.aniagu@university.edu",
        password="password123",
        first_name="Chiamaka",
        last_name="Aniagu",
        role="student",
        reg_id="ECO/2021/0982",
        department=eco,
        level=400,
        programme="B.Sc Economics",
        session="2025/2026",
        status="Active"
    )

    # Student 3 (for probation example)
    ibrahim = User.objects.create_user(
        username="PHY/2023/0214",
        email="i.musa@university.edu",
        password="password123",
        first_name="Ibrahim",
        last_name="Musa",
        role="student",
        reg_id="PHY/2023/0214",
        department=phy,
        level=200,
        programme="B.Sc Physics",
        session="2025/2026",
        status="Probation"
    )

    # Student 4 (for suspended example)
    ruth = User.objects.create_user(
        username="LAW/2024/0015",
        email="r.garba@university.edu",
        password="password123",
        first_name="Ruth",
        last_name="Garba",
        role="student",
        reg_id="LAW/2024/0015",
        department=law,
        level=200,
        programme="Bachelor of Laws",
        session="2025/2026",
        status="Suspended"
    )

    # Lecturer
    tunde = User.objects.create_user(
        username="t.okafor",
        email="t.okafor@university.edu",
        password="password123",
        first_name="Tunde",
        last_name="Okafor",
        role="lecturer",
        reg_id="staff-001",
        department=csc
    )

    # Additional Lecturer
    lawal = User.objects.create_user(
        username="a.lawal",
        email="a.lawal@university.edu",
        password="password123",
        first_name="Abubakar",
        last_name="Lawal",
        role="lecturer",
        reg_id="staff-004",
        department=csc
    )

    # Registrar
    funmi = User.objects.create_user(
        username="f.bello",
        email="f.bello@university.edu",
        password="password123",
        first_name="Funmilayo",
        last_name="Bello",
        role="registrar",
        reg_id="staff-002",
        department=acad
    )

    # Admin
    samuel = User.objects.create_user(
        username="s.adeyemi",
        email="s.adeyemi@university.edu",
        password="password123",
        first_name="Samuel",
        last_name="Adeyemi",
        role="admin",
        reg_id="staff-003",
        department=ict
    )

    # 3. Create Courses
    # 2nd Semester Courses (Current)
    csc301 = Course.objects.create(code="CSC 301", title="Data Structures & Algorithms", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    csc305 = Course.objects.create(code="CSC 305", title="Database Systems", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    csc311 = Course.objects.create(code="CSC 311", title="Operating Systems", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    csc313 = Course.objects.create(code="CSC 313", title="Software Engineering", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    csc401 = Course.objects.create(code="CSC 401", title="Distributed Systems", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    
    mth302 = Course.objects.create(code="MTH 302", title="Numerical Methods", units=3, department=csc, lecturer=None, semester="2nd Semester")
    gst301 = Course.objects.create(code="GST 301", title="Entrepreneurship Studies", units=2, department=csc, lecturer=None, semester="2nd Semester")

    # 1st Semester Courses (Historical/Future)
    csc101 = Course.objects.create(code="CSC 101", title="Introduction to Computer Science", units=3, department=csc, lecturer=tunde, semester="1st Semester")
    mth101 = Course.objects.create(code="MTH 101", title="General Mathematics I", units=3, department=csc, lecturer=None, semester="1st Semester")
    gst101 = Course.objects.create(code="GST 101", title="Use of English", units=2, department=csc, lecturer=None, semester="1st Semester")
    csc102 = Course.objects.create(code="CSC 102", title="Intro to Digital Design", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    mth102 = Course.objects.create(code="MTH 102", title="General Mathematics II", units=3, department=csc, lecturer=None, semester="2nd Semester")
    gst102 = Course.objects.create(code="GST 102", title="Use of Library", units=2, department=csc, lecturer=None, semester="2nd Semester")
    csc201 = Course.objects.create(code="CSC 201", title="Computer Programming I", units=3, department=csc, lecturer=tunde, semester="1st Semester")
    csc202 = Course.objects.create(code="CSC 202", title="Computer Programming II", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    csc203 = Course.objects.create(code="CSC 203", title="Discrete Structures", units=3, department=csc, lecturer=tunde, semester="1st Semester")
    mth201 = Course.objects.create(code="MTH 201", title="Mathematical Methods", units=3, department=csc, lecturer=None, semester="1st Semester")
    gst201 = Course.objects.create(code="GST 201", title="Social Science", units=2, department=csc, lecturer=None, semester="1st Semester")
    csc204 = Course.objects.create(code="CSC 204", title="Computer Architecture", units=3, department=csc, lecturer=tunde, semester="2nd Semester")
    csc303 = Course.objects.create(code="CSC 303", title="Compiler Construction", units=3, department=csc, lecturer=tunde, semester="1st Semester")
    csc307 = Course.objects.create(code="CSC 307", title="Computer Networks", units=3, department=csc, lecturer=tunde, semester="1st Semester")
    csc309 = Course.objects.create(code="CSC 309", title="Human Computer Interaction", units=3, department=csc, lecturer=tunde, semester="1st Semester")

    # 4. Seed completed courses for Adaeze to yield CGPA 4.62 (180 grade points over 39 units)
    # List of tuples: (course, score)
    completed_courses = [
        (csc101, 85),  # 3 units, A (15 pt)
        (mth101, 75),  # 3 units, A (15 pt)
        (gst101, 90),  # 2 units, A (10 pt)
        (csc102, 78),  # 3 units, A (15 pt)
        (mth102, 65),  # 3 units, B (12 pt)
        (gst102, 82),  # 2 units, A (10 pt)
        (csc201, 80),  # 3 units, A (15 pt)
        (csc202, 62),  # 3 units, B (12 pt)
        (csc203, 68),  # 3 units, B (12 pt)
        (mth201, 72),  # 3 units, A (15 pt)
        (gst201, 87),  # 2 units, A (10 pt)
        (csc303, 66),  # 3 units, B (12 pt)
        (csc307, 74),  # 3 units, A (15 pt)
        (csc309, 61),  # 3 units, B (12 pt)
    ]
    
    for course, score in completed_courses:
        Enrollment.objects.create(
            student=adaeze,
            course=course,
            semester=course.semester,
            session="2024/2025" if "101" in course.code or "102" in course.code else "2025/2026",
            status="Enrolled",
            score=score
        )

    # 5. Seed Current (Active) Registrations for 300L 2nd Semester
    Enrollment.objects.create(student=adaeze, course=csc301, semester="2nd Semester", session="2025/2026", status="Enrolled")
    Enrollment.objects.create(student=adaeze, course=csc305, semester="2nd Semester", session="2025/2026", status="Enrolled")
    Enrollment.objects.create(student=adaeze, course=csc311, semester="2nd Semester", session="2025/2026", status="Enrolled")
    Enrollment.objects.create(student=adaeze, course=mth302, semester="2nd Semester", session="2025/2026", status="Pending approval")
    Enrollment.objects.create(student=adaeze, course=gst301, semester="2nd Semester", session="2025/2026", status="Enrolled")
    Enrollment.objects.create(student=adaeze, course=csc313, semester="2nd Semester", session="2025/2026", status="Enrolled")

    # 6. Seed other students' mock enrollments
    Enrollment.objects.create(student=chiamaka, course=csc301, semester="2nd Semester", session="2025/2026", status="Enrolled")
    Enrollment.objects.create(student=ibrahim, course=csc301, semester="2nd Semester", session="2025/2026", status="Enrolled")

    # 7. Transcript Request
    TranscriptRequest.objects.create(
        student=adaeze,
        reference="TR-7E29-4401",
        status="Approved"
    )
    TranscriptRequest.objects.create(
        student=chiamaka,
        reference="TR-8B41-2139",
        status="Pending"
    )

    # 8. Audit Logs
    AuditLog.objects.create(user=samuel, action="Created user CSC/2022/0417 (Adaeze Okoro)")
    AuditLog.objects.create(user=funmi, action="Approved course registration for CSC/2022/0417")
    AuditLog.objects.create(user=tunde, action="Result finalized for CSC 301")
    AuditLog.objects.create(user=adaeze, action="Registered for MTH 302")
    AuditLog.objects.create(user=samuel, action="Generated transcript TR-7E29-4401")

    print("Database seeding completed successfully.")

if __name__ == '__main__':
    run()

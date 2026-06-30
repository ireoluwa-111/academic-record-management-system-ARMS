from django.test import TestCase
from django.contrib.auth import get_user_model
from records.models import Department, Course, Enrollment, TranscriptRequest, AuditLog

User = get_user_model()

class ARMSModelTests(TestCase):
    def setUp(self):
        # Create department
        self.dept = Department.objects.create(code="CSC", name="Computer Science")
        
        # Create user
        self.student = User.objects.create_user(
            username="CSC/2022/0417",
            email="adaeze@test.com",
            password="password123",
            role="student",
            reg_id="CSC/2022/0417",
            department=self.dept
        )

        # Create lecturer
        self.lecturer = User.objects.create_user(
            username="tunde",
            email="tunde@test.com",
            password="password123",
            role="lecturer",
            reg_id="staff-001",
            department=self.dept
        )

        # Create course
        self.course = Course.objects.create(
            code="CSC 301",
            title="Data Structures",
            units=3,
            department=self.dept,
            lecturer=self.lecturer,
            semester="1st Semester"
        )

    def test_grade_calculation(self):
        # Test A grade (>= 70)
        e1 = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            score=85,
            semester="1st Semester",
            session="2025/2026",
            status="Enrolled"
        )
        self.assertEqual(e1.grade, 'A')
        self.assertEqual(e1.grade_points(), 5)

        # Test B grade (60 - 69)
        e1.score = 65
        e1.save()
        self.assertEqual(e1.grade, 'B')
        self.assertEqual(e1.grade_points(), 4)

        # Test F grade (< 40)
        e1.score = 35
        e1.save()
        self.assertEqual(e1.grade, 'F')
        self.assertEqual(e1.grade_points(), 0)

    def test_cgpa_calculation(self):
        course2 = Course.objects.create(
            code="CSC 302",
            title="Databases",
            units=4,
            department=self.dept,
            lecturer=self.lecturer,
            semester="1st Semester"
        )

        # Enrollments with scores
        # Course 1: 3 units, score 80 (Grade A, points 5) -> 15 grade points
        Enrollment.objects.create(
            student=self.student,
            course=self.course,
            score=80,
            semester="1st Semester",
            session="2025/2026",
            status="Enrolled"
        )
        
        # Course 2: 4 units, score 65 (Grade B, points 4) -> 16 grade points
        Enrollment.objects.create(
            student=self.student,
            course=course2,
            score=65,
            semester="1st Semester",
            session="2025/2026",
            status="Enrolled"
        )

        # CGPA = (15 + 16) / (3 + 4) = 31 / 7 = 4.43
        completed = Enrollment.objects.filter(student=self.student, status='Enrolled', score__isnull=False)
        total_units = sum(e.course.units for e in completed)
        total_points = sum(e.course.units * e.grade_points() for e in completed)
        cgpa = round(total_points / total_units, 2)
        
        self.assertEqual(cgpa, 4.43)

class ARMSViewAccessTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code="CSC", name="Computer Science")
        
        # Student
        self.student = User.objects.create_user(
            username="student1",
            email="student1@test.com",
            password="password123",
            role="student",
            reg_id="student1",
            department=self.dept
        )
        
        # Lecturer
        self.lecturer = User.objects.create_user(
            username="lecturer1",
            email="lecturer1@test.com",
            password="password123",
            role="lecturer",
            reg_id="lecturer1",
            department=self.dept
        )
        
        # Registrar
        self.registrar = User.objects.create_user(
            username="registrar1",
            email="registrar1@test.com",
            password="password123",
            role="registrar",
            reg_id="registrar1"
        )
        
        # Admin
        self.admin = User.objects.create_user(
            username="admin1",
            email="admin1@test.com",
            password="password123",
            role="admin",
            reg_id="admin1"
        )

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/student/')
        self.assertRedirects(response, '/login/?next=/dashboard/student/')

    def test_student_dashboard_tabs_and_posts(self):
        self.client.login(username="student1", password="password123")
        
        # Test tab GET requests
        for tab in ['dashboard', 'profile', 'courses', 'results', 'transcript', 'notifications', 'settings']:
            response = self.client.get(f'/dashboard/student/?tab={tab}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['active_tab'], tab)
            self.assertContains(response, 'student1') # Verify student ID appears in sidebar / header
            
        # Test profile update
        response = self.client.post('/dashboard/student/', {
            'action': 'profile_update',
            'firstName': 'Ada',
            'lastName': 'Lovelace',
            'email': 'ada@lovelace.com',
            'programme': 'B.Sc Mathematics'
        })
        self.assertRedirects(response, '/dashboard/student/?tab=profile&success=profile')
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Ada')
        self.assertEqual(self.student.last_name, 'Lovelace')
        
        # Test password change
        response = self.client.post('/dashboard/student/', {
            'action': 'change_password',
            'oldPassword': 'password123',
            'newPassword': 'newpassword456',
            'confirmPassword': 'newpassword456'
        })
        self.assertRedirects(response, '/dashboard/student/?tab=settings&success=password')
        
        # Verify password updated
        self.student.refresh_from_db()
        self.assertTrue(self.student.check_password('newpassword456'))

    def test_lecturer_dashboard_tabs_and_posts(self):
        self.client.login(username="lecturer1", password="password123")
        
        # Test tab GET requests
        for tab in ['dashboard', 'profile', 'courses', 'rosters', 'results', 'settings']:
            response = self.client.get(f'/dashboard/lecturer/?tab={tab}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['active_tab'], tab)
            
        # Test profile update
        response = self.client.post('/dashboard/lecturer/', {
            'action': 'profile_update',
            'firstName': 'Alan',
            'lastName': 'Turing',
            'email': 'alan@turing.com'
        })
        self.assertRedirects(response, '/dashboard/lecturer/?tab=profile&success=profile')
        self.lecturer.refresh_from_db()
        self.assertEqual(self.lecturer.first_name, 'Alan')
        
    def test_registrar_dashboard_tabs_and_posts(self):
        self.client.login(username="registrar1", password="password123")
        
        # Test tab GET requests
        for tab in ['dashboard', 'records', 'courses', 'oversight', 'transcripts', 'settings']:
            response = self.client.get(f'/dashboard/registrar/?tab={tab}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['active_tab'], tab)
            
        # Test create course
        response = self.client.post('/dashboard/registrar/', {
            'action': 'create_course',
            'courseCode': 'CSC 303',
            'courseTitle': 'Software Engineering',
            'courseUnits': 3,
            'courseDept': self.dept.id,
            'courseLecturer': self.lecturer.id,
            'courseSemester': '2nd Semester'
        })
        self.assertRedirects(response, '/dashboard/registrar/?tab=courses&success=course')
        self.assertTrue(Course.objects.filter(code='CSC 303').exists())

    def test_admin_dashboard_tabs_and_posts(self):
        self.client.login(username="admin1", password="password123")
        
        # Test tab GET requests
        for tab in ['dashboard', 'users', 'roles', 'departments', 'settings']:
            response = self.client.get(f'/dashboard/admin/?tab={tab}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['active_tab'], tab)
            
        # Test create department
        response = self.client.post('/dashboard/admin/', {
            'action': 'create_department',
            'deptCode': 'MTH',
            'deptName': 'Mathematics'
        })
        self.assertRedirects(response, '/dashboard/admin/?tab=departments&success=dept')
        self.assertTrue(Department.objects.filter(code='MTH').exists())
        
        # Test status dropdown check
        response = self.client.post('/admin-edit-user-status/', {
            'userId': self.student.id,
            'status': 'Suspended'
        })
        self.assertRedirects(response, '/dashboard/admin/?tab=users')
        self.student.refresh_from_db()
        self.assertEqual(self.student.status, 'Suspended')

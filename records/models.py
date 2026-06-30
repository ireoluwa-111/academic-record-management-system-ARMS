from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Registrar'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    reg_id = models.CharField(max_length=50, unique=True, verbose_name="Matric / Staff ID")
    
    # Student and Lecturer custom fields
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.IntegerField(default=100, blank=True, null=True)
    programme = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=20, default="2025/2026", blank=True, null=True)
    status = models.CharField(max_length=20, default="Active") # Active, Probation, Suspended

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.reg_id})"

class Course(models.Model):
    SEMESTER_CHOICES = (
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
    )
    code = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=150)
    units = models.IntegerField(default=3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'lecturer'}, related_name='courses_taught')
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='1st Semester')

    def __str__(self):
        return f"{self.code} - {self.title}"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('Pending approval', 'Pending approval'),
        ('Enrolled', 'Enrolled'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField(max_length=20, default='1st Semester')
    session = models.CharField(max_length=20, default='2025/2026')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending approval')
    score = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course', 'session')

    def save(self, *args, **kwargs):
        if self.score is not None:
            score = self.score
            if score >= 70:
                self.grade = 'A'
            elif score >= 60:
                self.grade = 'B'
            elif score >= 50:
                self.grade = 'C'
            elif score >= 45:
                self.grade = 'D'
            elif score >= 40:
                self.grade = 'E'
            else:
                self.grade = 'F'
        else:
            self.grade = None
        super().save(*args, **kwargs)

    def grade_points(self):
        points = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        return points.get(self.grade, 0) if self.grade else 0

    def __str__(self):
        return f"{self.student.reg_id} - {self.course.code} ({self.status})"

class TranscriptRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='transcript_requests')
    reference = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} - {self.student.reg_id} ({self.status})"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user.reg_id if self.user else 'System'}: {self.action}"

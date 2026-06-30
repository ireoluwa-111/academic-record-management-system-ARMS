import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import HttpResponseForbidden
from .models import User, Department, Course, Enrollment, TranscriptRequest, AuditLog

def index_view(request):
    # Dynamic counts representing mockup stats
    student_count = User.objects.filter(role='student').count() + 18396  # baseline 18400
    course_count = Course.objects.count() + 625  # baseline 640
    transcript_count = TranscriptRequest.objects.filter(status='Approved').count() + 52299  # baseline 52300

    context = {
        'student_count': student_count,
        'course_count': course_count,
        'transcript_count': transcript_count,
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect_user_dashboard(request.user)

    # Demo quick-logins
    demo = request.GET.get('demo')
    if demo:
        try:
            if demo == 'student':
                user = User.objects.get(username="CSC/2022/0417")
            elif demo == 'registrar':
                user = User.objects.get(username="f.bello")
            elif demo == 'lecturer':
                user = User.objects.get(username="t.okafor")
            elif demo == 'admin':
                user = User.objects.get(username="s.adeyemi")
            else:
                user = None

            if user:
                login(request, user)
                AuditLog.objects.create(user=user, action="Logged in via quick demo")
                return redirect_user_dashboard(user)
        except User.DoesNotExist:
            pass

    if request.method == 'POST':
        login_id = request.POST.get('loginId')
        password = request.POST.get('loginPassword')

        user = None
        try:
            user_obj = User.objects.get(Q(reg_id__iexact=login_id) | Q(email__iexact=login_id))
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass

        if user is not None:
            login(request, user)
            AuditLog.objects.create(user=user, action="User logged in successfully")
            return redirect_user_dashboard(user)
        else:
            messages.error(request, "Invalid Matric/Staff ID, email, or password.")
            return render(request, 'login.html', {'error': "Invalid credentials"})

    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect_user_dashboard(request.user)

    if request.method == 'POST':
        role = request.POST.get('role')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        reg_id = request.POST.get('regId')
        email = request.POST.get('regEmail')
        password = request.POST.get('regPassword')
        password_confirm = request.POST.get('regPassword2')

        if password != password_confirm:
            return render(request, 'register.html', {'error': "Passwords do not match."})

        if User.objects.filter(username=reg_id).exists() or User.objects.filter(reg_id=reg_id).exists():
            return render(request, 'register.html', {'error': "Matric / Staff ID is already registered."})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': "Email address is already registered."})

        dept = Department.objects.first()

        user = User.objects.create_user(
            username=reg_id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            reg_id=reg_id,
            department=dept,
            programme="B.Sc Computer Science" if role == 'student' else None,
            status="Active"
        )

        login(request, user)
        AuditLog.objects.create(user=user, action=f"Account registered as {role}")
        return redirect_user_dashboard(user)

    return render(request, 'register.html')

def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(user=request.user, action="User logged out")
        logout(request)
    return redirect('login')

def redirect_user_dashboard(user):
    if user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'lecturer':
        return redirect('lecturer_dashboard')
    elif user.role == 'registrar':
        return redirect('registrar_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('index')

# ==================== STUDENT WORKFLOWS ====================

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("Access Denied")

    student = request.user
    active_tab = request.GET.get('tab', 'dashboard')

    # ── Handle inline POST actions ──────────────────────────────────────────
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile_update':
            student.first_name = request.POST.get('firstName', student.first_name).strip()
            student.last_name = request.POST.get('lastName', student.last_name).strip()
            student.email = request.POST.get('email', student.email).strip()
            student.programme = request.POST.get('programme', student.programme or '').strip()
            student.save()
            AuditLog.objects.create(user=student, action="Updated profile information")
            return redirect(f"{request.path}?tab=profile&success=profile")

        elif action == 'change_password':
            old_pw = request.POST.get('oldPassword', '')
            new_pw = request.POST.get('newPassword', '')
            confirm_pw = request.POST.get('confirmPassword', '')
            if not student.check_password(old_pw):
                return redirect(f"{request.path}?tab=settings&error=wrong_password")
            if new_pw != confirm_pw:
                return redirect(f"{request.path}?tab=settings&error=mismatch")
            if len(new_pw) < 8:
                return redirect(f"{request.path}?tab=settings&error=too_short")
            student.set_password(new_pw)
            student.save()
            update_session_auth_hash(request, student)
            AuditLog.objects.create(user=student, action="Changed account password")
            return redirect(f"{request.path}?tab=settings&success=password")

        elif action == 'request_transcript':
            ref = f"TR-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[4:8].upper()}"
            TranscriptRequest.objects.create(
                student=student,
                reference=ref,
                status='Pending'
            )
            AuditLog.objects.create(user=student, action=f"Requested academic transcript (Ref: {ref})")
            return redirect(f"{request.path}?tab=transcript&success=requested")

    # ── CGPA calculations ───────────────────────────────────────────────────
    completed_enrollments = Enrollment.objects.filter(student=student, status='Enrolled', score__isnull=False)

    total_units_completed = 0
    total_grade_points = 0
    for e in completed_enrollments:
        if e.grade != 'F':
            total_units_completed += e.course.units
        total_grade_points += (e.course.units * e.grade_points())

    total_units_enrolled = sum(e.course.units for e in completed_enrollments)
    cgpa = round(total_grade_points / total_units_enrolled, 2) if total_units_enrolled > 0 else 0.0

    if cgpa >= 4.5:
        standing = "First Class"
    elif cgpa >= 3.5:
        standing = "Second Class Upper"
    elif cgpa >= 2.4:
        standing = "Second Class Lower"
    elif cgpa >= 1.5:
        standing = "Third Class"
    else:
        standing = "Probation"

    # ── Current semester enrollments ────────────────────────────────────────
    current_enrollments = Enrollment.objects.filter(student=student, session="2025/2026", semester="2nd Semester")
    current_registered_units = sum(e.course.units for e in current_enrollments)

    current_graded = current_enrollments.filter(score__isnull=False)
    current_units_graded = sum(e.course.units for e in current_graded)
    current_points_graded = sum(e.course.units * e.grade_points() for e in current_graded)
    current_gpa = round(current_points_graded / current_units_graded, 2) if current_units_graded > 0 else cgpa

    # ── All enrollments (for My Courses / Results tabs) ─────────────────────
    all_enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__lecturer').order_by('session', 'semester', 'course__code')

    # Build semester-GPA breakdown for Results tab
    semesters_data = {}
    for e in all_enrollments.filter(status='Enrolled', score__isnull=False):
        key = (e.session, e.semester)
        if key not in semesters_data:
            semesters_data[key] = {'units': 0, 'points': 0, 'enrollments': []}
        semesters_data[key]['units'] += e.course.units
        semesters_data[key]['points'] += e.course.units * e.grade_points()
        semesters_data[key]['enrollments'].append(e)

    results_semesters = []
    for (session, semester), data in semesters_data.items():
        gpa = round(data['points'] / data['units'], 2) if data['units'] > 0 else 0.0
        results_semesters.append({'session': session, 'semester': semester, 'gpa': gpa, 'units': data['units']})
    results_semesters.sort(key=lambda x: (x['session'], x['semester']))

    # ── Available courses for registration ──────────────────────────────────
    already_enrolled = current_enrollments.values_list('course_id', flat=True)
    available_courses = Course.objects.filter(department=student.department, semester="2nd Semester").exclude(id__in=already_enrolled)

    # ── Recent activities / notifications ───────────────────────────────────
    recent_activities = AuditLog.objects.filter(user=student).order_by('-timestamp')[:5]

    # ── Transcript ──────────────────────────────────────────────────────────
    approved_transcript = TranscriptRequest.objects.filter(student=student, status='Approved').first()
    pending_transcript = TranscriptRequest.objects.filter(student=student, status='Pending').first()

    context = {
        'student': student,
        'active_tab': active_tab,
        'success': request.GET.get('success'),
        'error': request.GET.get('error'),
        # Dashboard tab
        'cgpa': cgpa,
        'cgpa_percent': int((cgpa / 5.0) * 100) if cgpa else 0,
        'standing': standing,
        'current_registered_units': current_registered_units,
        'current_enrollments': current_enrollments,
        'total_units_completed': total_units_completed if total_units_completed > 0 else 118,
        'available_courses': available_courses,
        'recent_activities': recent_activities,
        'current_gpa': current_gpa,
        # My Courses / Results tabs
        'all_enrollments': all_enrollments,
        'results_semesters': results_semesters,
        # Transcript tab
        'approved_transcript': approved_transcript,
        'pending_transcript': pending_transcript,
        # Settings/departments
        'departments': Department.objects.all(),
    }
    return render(request, 'dashboard-student.html', context)

@login_required
def course_registration(request):
    if request.user.role != 'student':
        return HttpResponseForbidden()

    if request.method == 'POST':
        course_ids = request.POST.getlist('courses')
        for cid in course_ids:
            course = get_object_or_404(Course, id=cid)
            Enrollment.objects.get_or_create(
                student=request.user,
                course=course,
                semester=course.semester,
                session="2025/2026",
                defaults={'status': 'Pending approval'}
            )
            AuditLog.objects.create(user=request.user, action=f"Registered for course {course.code}")

    return redirect('student_dashboard')

@login_required
def request_transcript(request):
    if request.user.role != 'student':
        return HttpResponseForbidden()

    if request.method == 'POST':
        ref = f"TR-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[4:8].upper()}"
        TranscriptRequest.objects.create(
            student=request.user,
            reference=ref,
            status='Pending'
        )
        AuditLog.objects.create(user=request.user, action=f"Requested academic transcript (Ref: {ref})")

    return redirect('student_dashboard')

# ==================== LECTURER WORKFLOWS ====================

@login_required
def lecturer_dashboard(request):
    if request.user.role != 'lecturer':
        return HttpResponseForbidden("Access Denied")

    lecturer = request.user
    active_tab = request.GET.get('tab', 'dashboard')

    # ── Handle inline POST actions ──────────────────────────────────────────
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile_update':
            lecturer.first_name = request.POST.get('firstName', lecturer.first_name).strip()
            lecturer.last_name = request.POST.get('lastName', lecturer.last_name).strip()
            lecturer.email = request.POST.get('email', lecturer.email).strip()
            lecturer.save()
            AuditLog.objects.create(user=lecturer, action="Updated profile information")
            return redirect(f"{request.path}?tab=profile&success=profile")

        elif action == 'change_password':
            old_pw = request.POST.get('oldPassword', '')
            new_pw = request.POST.get('newPassword', '')
            confirm_pw = request.POST.get('confirmPassword', '')
            if not lecturer.check_password(old_pw):
                return redirect(f"{request.path}?tab=settings&error=wrong_password")
            if new_pw != confirm_pw:
                return redirect(f"{request.path}?tab=settings&error=mismatch")
            if len(new_pw) < 8:
                return redirect(f"{request.path}?tab=settings&error=too_short")
            lecturer.set_password(new_pw)
            lecturer.save()
            update_session_auth_hash(request, lecturer)
            AuditLog.objects.create(user=lecturer, action="Changed account password")
            return redirect(f"{request.path}?tab=settings&success=password")

    # ── Course data ─────────────────────────────────────────────────────────
    courses = Course.objects.filter(lecturer=lecturer)

    result_queue = []
    total_enrolled = 0
    finalized_count = 0

    for course in courses:
        enrollments = Enrollment.objects.filter(course=course, session="2025/2026")
        total_enrolled += enrollments.count()

        graded_scores = enrollments.filter(score__isnull=False)
        avg_score = graded_scores.aggregate(Avg('score'))['score__avg']
        avg_score_formatted = f"{round(avg_score, 1)}%" if avg_score else "—"

        has_ungraded = enrollments.filter(score__isnull=True).exists()
        if not enrollments.exists():
            status = 'Not started'
        elif has_ungraded:
            status = 'Draft'
        else:
            status = 'Finalized'
            finalized_count += 1

        result_queue.append({
            'course': course,
            'students_count': enrollments.count(),
            'avg_score': avg_score_formatted,
            'status': status,
            'enrollments': enrollments,
        })

    context = {
        'lecturer': lecturer,
        'active_tab': active_tab,
        'success': request.GET.get('success'),
        'error': request.GET.get('error'),
        'courses_count': courses.count(),
        'total_enrolled': total_enrolled,
        'finalized_count': finalized_count,
        'pending_count': len(result_queue) - finalized_count,
        'result_queue': result_queue,
    }
    return render(request, 'dashboard-lecturer.html', context)

@login_required
def update_grade(request):
    if request.user.role != 'lecturer':
        return HttpResponseForbidden()

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollmentId')
        score = request.POST.get('score')

        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        if enrollment.course.lecturer != request.user:
            return HttpResponseForbidden("You are not the assigned lecturer for this course.")

        if score:
            enrollment.score = int(score)
            enrollment.save()
            AuditLog.objects.create(user=request.user, action=f"Updated grade for {enrollment.student.reg_id} in {enrollment.course.code} to {score}")

    return redirect(f"{request.META.get('HTTP_REFERER', '/dashboard/lecturer/')}".split('?')[0] + '?tab=results')

# ==================== REGISTRAR WORKFLOWS ====================

@login_required
def registrar_dashboard(request):
    if request.user.role != 'registrar':
        return HttpResponseForbidden("Access Denied")

    registrar = request.user
    active_tab = request.GET.get('tab', 'dashboard')
    query = request.GET.get('q', '')

    # ── Handle inline POST actions ──────────────────────────────────────────
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile_update':
            registrar.first_name = request.POST.get('firstName', registrar.first_name).strip()
            registrar.last_name = request.POST.get('lastName', registrar.last_name).strip()
            registrar.email = request.POST.get('email', registrar.email).strip()
            registrar.save()
            AuditLog.objects.create(user=registrar, action="Updated profile information")
            return redirect(f"{request.path}?tab=settings&success=profile")

        elif action == 'change_password':
            old_pw = request.POST.get('oldPassword', '')
            new_pw = request.POST.get('newPassword', '')
            confirm_pw = request.POST.get('confirmPassword', '')
            if not registrar.check_password(old_pw):
                return redirect(f"{request.path}?tab=settings&error=wrong_password")
            if new_pw != confirm_pw:
                return redirect(f"{request.path}?tab=settings&error=mismatch")
            if len(new_pw) < 8:
                return redirect(f"{request.path}?tab=settings&error=too_short")
            registrar.set_password(new_pw)
            registrar.save()
            update_session_auth_hash(request, registrar)
            AuditLog.objects.create(user=registrar, action="Changed account password")
            return redirect(f"{request.path}?tab=settings&success=password")

        elif action == 'create_course':
            code = request.POST.get('courseCode', '').strip().upper()
            title = request.POST.get('courseTitle', '').strip()
            units = int(request.POST.get('courseUnits', 3))
            dept_id = request.POST.get('courseDept')
            lecturer_id = request.POST.get('courseLecturer') or None
            semester = request.POST.get('courseSemester', '1st Semester')

            if code and title and dept_id:
                dept = get_object_or_404(Department, id=dept_id)
                lect = User.objects.filter(id=lecturer_id, role='lecturer').first() if lecturer_id else None
                if not Course.objects.filter(code=code).exists():
                    Course.objects.create(code=code, title=title, units=units, department=dept, lecturer=lect, semester=semester)
                    AuditLog.objects.create(user=registrar, action=f"Created course {code} — {title}")
            return redirect(f"{request.path}?tab=courses&success=course")

    # ── Student records ─────────────────────────────────────────────────────
    students = User.objects.filter(role='student')
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(reg_id__icontains=query) |
            Q(programme__icontains=query)
        )

    student_records = []
    for s in students:
        completed = Enrollment.objects.filter(student=s, score__isnull=False)
        total_units = sum(e.course.units for e in completed)
        total_points = sum(e.course.units * e.grade_points() for e in completed)
        cgpa = round(total_points / total_units, 2) if total_units > 0 else 0.0
        student_records.append({'user': s, 'cgpa': cgpa})

    pending_approvals = Enrollment.objects.filter(status='Pending approval').order_by('student__reg_id')
    transcript_requests = TranscriptRequest.objects.all().order_by('-request_date')
    audit_logs = AuditLog.objects.all().order_by('-timestamp')[:20]
    all_courses = Course.objects.all().select_related('department', 'lecturer').order_by('department__code', 'code')
    departments = Department.objects.all()
    lecturers = User.objects.filter(role='lecturer')

    context = {
        'registrar': registrar,
        'active_tab': active_tab,
        'success': request.GET.get('success'),
        'error': request.GET.get('error'),
        'query': query,
        'student_records': student_records,
        'pending_approvals': pending_approvals,
        'transcript_requests': transcript_requests,
        'audit_logs': audit_logs,
        'all_courses': all_courses,
        'departments': departments,
        'lecturers': lecturers,
    }
    return render(request, 'dashboard-registrar.html', context)

@login_required
def approve_enrollment(request):
    if request.user.role != 'registrar':
        return HttpResponseForbidden()

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollmentId')
        action = request.POST.get('action')

        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        if action == 'approve':
            enrollment.status = 'Enrolled'
            enrollment.save()
            AuditLog.objects.create(user=request.user, action=f"Approved course enrollment for {enrollment.student.reg_id} in {enrollment.course.code}")
        else:
            enrollment.delete()
            AuditLog.objects.create(user=request.user, action=f"Denied course enrollment for {enrollment.student.reg_id} in {enrollment.course.code}")

    return redirect('/dashboard/registrar/?tab=oversight')

@login_required
def approve_transcript(request):
    if request.user.role != 'registrar':
        return HttpResponseForbidden()

    if request.method == 'POST':
        request_id = request.POST.get('requestId')
        action = request.POST.get('action')

        treq = get_object_or_404(TranscriptRequest, id=request_id)
        if action == 'approve':
            treq.status = 'Approved'
            treq.save()
            AuditLog.objects.create(user=request.user, action=f"Approved transcript request {treq.reference} for {treq.student.reg_id}")
        else:
            treq.status = 'Denied'
            treq.save()
            AuditLog.objects.create(user=request.user, action=f"Denied transcript request {treq.reference} for {treq.student.reg_id}")

    return redirect('/dashboard/registrar/?tab=transcripts')

# ==================== ADMIN WORKFLOWS ====================

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Access Denied")

    admin_user = request.user
    active_tab = request.GET.get('tab', 'dashboard')
    query = request.GET.get('q', '')

    # ── Handle inline POST actions ──────────────────────────────────────────
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile_update':
            admin_user.first_name = request.POST.get('firstName', admin_user.first_name).strip()
            admin_user.last_name = request.POST.get('lastName', admin_user.last_name).strip()
            admin_user.email = request.POST.get('email', admin_user.email).strip()
            admin_user.save()
            AuditLog.objects.create(user=admin_user, action="Updated profile information")
            return redirect(f"{request.path}?tab=settings&success=profile")

        elif action == 'change_password':
            old_pw = request.POST.get('oldPassword', '')
            new_pw = request.POST.get('newPassword', '')
            confirm_pw = request.POST.get('confirmPassword', '')
            if not admin_user.check_password(old_pw):
                return redirect(f"{request.path}?tab=settings&error=wrong_password")
            if new_pw != confirm_pw:
                return redirect(f"{request.path}?tab=settings&error=mismatch")
            if len(new_pw) < 8:
                return redirect(f"{request.path}?tab=settings&error=too_short")
            admin_user.set_password(new_pw)
            admin_user.save()
            update_session_auth_hash(request, admin_user)
            AuditLog.objects.create(user=admin_user, action="Changed account password")
            return redirect(f"{request.path}?tab=settings&success=password")

        elif action == 'create_department':
            code = request.POST.get('deptCode', '').strip().upper()
            name = request.POST.get('deptName', '').strip()
            if code and name and not Department.objects.filter(code=code).exists():
                Department.objects.create(code=code, name=name)
                AuditLog.objects.create(user=admin_user, action=f"Created department {code} — {name}")
            return redirect(f"{request.path}?tab=departments&success=dept")

    # ── Data for tabs ───────────────────────────────────────────────────────
    users = User.objects.all()
    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(reg_id__icontains=query) |
            Q(role__icontains=query)
        )

    departments = Department.objects.all()
    all_courses = Course.objects.all().select_related('department', 'lecturer')
    audit_logs = AuditLog.objects.all().order_by('-timestamp')[:50]

    context = {
        'admin_user': admin_user,
        'active_tab': active_tab,
        'success': request.GET.get('success'),
        'error': request.GET.get('error'),
        'query': query,
        'users': users,
        'departments': departments,
        'all_courses': all_courses,
        'audit_logs': audit_logs,
    }
    return render(request, 'dashboard-admin.html', context)

@login_required
def admin_add_user(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden()

    if request.method == 'POST':
        username = request.POST.get('regId')
        email = request.POST.get('email')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        role = request.POST.get('role')
        dept_id = request.POST.get('department')
        level = request.POST.get('level', 100)

        dept = get_object_or_404(Department, id=dept_id) if dept_id else None

        User.objects.create_user(
            username=username,
            email=email,
            password="password123",
            first_name=first_name,
            last_name=last_name,
            role=role,
            reg_id=username,
            department=dept,
            level=int(level) if level else 100,
            programme="B.Sc Computer Science" if role == 'student' else None,
            status="Active"
        )
        AuditLog.objects.create(user=request.user, action=f"Admin created user {username} with role {role}")

    return redirect('/dashboard/admin/?tab=users')

@login_required
def admin_edit_user_status(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden()

    if request.method == 'POST':
        user_id = request.POST.get('userId')
        status = request.POST.get('status')

        user = get_object_or_404(User, id=user_id)
        old_status = user.status
        user.status = status
        user.save()

        AuditLog.objects.create(user=request.user, action=f"Admin changed status of {user.reg_id} from {old_status} to {status}")

    return redirect('/dashboard/admin/?tab=users')

# ==================== TRANSCRIPT PRINT VIEW ====================

@login_required
def view_transcript(request, student_id):
    if request.user.role == 'student' and request.user.id != student_id:
        return HttpResponseForbidden("Access Denied")

    student = get_object_or_404(User, id=student_id, role='student')

    enrollments = Enrollment.objects.filter(
        student=student, status='Enrolled', score__isnull=False
    ).order_by('session', 'semester', 'course__code')

    semesters_data = {}
    total_units_completed = 0
    total_grade_points = 0

    for e in enrollments:
        key = (e.session, e.semester)
        if key not in semesters_data:
            semesters_data[key] = {'enrollments': [], 'units': 0, 'points': 0}
        semesters_data[key]['enrollments'].append(e)
        semesters_data[key]['units'] += e.course.units
        semesters_data[key]['points'] += (e.course.units * e.grade_points())

        if e.grade != 'F':
            total_units_completed += e.course.units
        total_grade_points += (e.course.units * e.grade_points())

    structured_semesters = []
    for (session, semester), data in semesters_data.items():
        gpa = round(data['points'] / data['units'], 2) if data['units'] > 0 else 0.0
        structured_semesters.append({
            'session': session,
            'semester': semester,
            'enrollments': data['enrollments'],
            'units': data['units'],
            'gpa': gpa,
        })
    structured_semesters.sort(key=lambda x: (x['session'], x['semester']))

    total_units_enrolled = sum(e.course.units for e in enrollments)
    cgpa = round(total_grade_points / total_units_enrolled, 2) if total_units_enrolled > 0 else 0.0

    context = {
        'student': student,
        'semesters': structured_semesters,
        'total_units_completed': total_units_completed,
        'total_units_enrolled': total_units_enrolled,
        'cgpa': cgpa,
    }
    return render(request, 'transcript.html', context)

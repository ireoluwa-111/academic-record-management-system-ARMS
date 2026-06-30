from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login.html', views.login_view, name='login_html'), # support direct relative links from mockup
    path('login/', views.login_view, name='login'),
    path('register.html', views.register_view, name='register_html'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard-student.html', views.student_dashboard, name='student_dashboard_html'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard-lecturer.html', views.lecturer_dashboard, name='lecturer_dashboard_html'),
    path('dashboard/lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('dashboard-registrar.html', views.registrar_dashboard, name='registrar_dashboard_html'),
    path('dashboard/registrar/', views.registrar_dashboard, name='registrar_dashboard'),
    path('dashboard-admin.html', views.admin_dashboard, name='admin_dashboard_html'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # Actions
    path('course-register/', views.course_registration, name='course_registration'),
    path('request-transcript/', views.request_transcript, name='request_transcript'),
    path('update-grade/', views.update_grade, name='update_grade'),
    path('approve-enrollment/', views.approve_enrollment, name='approve_enrollment'),
    path('approve-transcript/', views.approve_transcript, name='approve_transcript'),
    path('admin-add-user/', views.admin_add_user, name='admin_add_user'),
    path('admin-edit-user-status/', views.admin_edit_user_status, name='admin_edit_user_status'),
    path('transcript/<int:student_id>/', views.view_transcript, name='view_transcript'),
]

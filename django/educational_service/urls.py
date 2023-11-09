from django.urls import path
from educational_service import views

urlpatterns = [
    path('', views.index, name="home"),
    path('student/<int:student_id>', views.student),
    path('university/<int:university_id>', views.university),
    path('student/create', views.create_student),
    path('university/create', views.create_university),
    path('student/delete/<int:student_id>', views.delete_student),
    path('university/delete/<int:university_id>', views.delete_university),
    path('student/', views.students_list),
    path('university/', views.university_list),
    path('student/update/<int:student_id>/<str:field_name>', views.student_update),
    path('university/update/<int:university_id>/<str:field_name>', views.university_update),
    path('student/update', views.updator_student),
    path('university/update', views.updator_university)
]

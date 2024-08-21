from django.urls import path
from .views import reservar_cita, ver_horarios, historial_citas, buscar_medicos, patient_login, patient_logout, dashboard, create_patient

urlpatterns = [
    path('login/', patient_login, name='login'),
    path('logout/', patient_logout, name='logout'),
    path('', dashboard, name='dashboard'),
    path('register/', create_patient, name='register'),
    # path('', base),
    # path('new/', create_task, name='create_task'),
    path('medicos/', buscar_medicos, name='buscar_medicos'),
    path('cita/reservar/<int:medico_id>/', reservar_cita, name='reservar_cita'),
    path('cita/horarios/<int:medico_id>/', ver_horarios, name='ver_horarios'),
    path('citas/historial/', historial_citas, name='historial_citas'),
]
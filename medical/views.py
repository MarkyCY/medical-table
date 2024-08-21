from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, Patient, Specialization
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
# def base(request):
#     speci = Specialization.objects.all()
#     return render(request, 'base.html', {'speci': speci})

# def create_task(request):
#     Specialization(name=request.POST['title'], description=request.POST['content']).save()
#     return redirect('/test/')


def create_patient(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = make_password(request.POST['password'])  # Cifrar la contraseña

        # Verificar si el email ya está registrado
        if Patient.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
        else:
            patient = Patient(name=name, email=email, phone=phone, password=password)
            patient.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige al login después del registro exitoso

    return render(request, 'register.html')


def patient_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            patient = Patient.objects.get(email=email)
            if check_password(password, patient.password):
                # Aquí podrías usar Django's session framework para almacenar la información del paciente
                request.session['patient_id'] = patient.id
                request.session['patient_name'] = patient.name
                return redirect('dashboard')  # Cambia 'dashboard' por la URL a la que quieras redirigir después de iniciar sesión
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Patient.DoesNotExist:
            messages.error(request, 'El paciente no existe')

    return render(request, 'login.html')


def patient_logout(request):
    if 'patient_id' in request.session:
        del request.session['patient_id']
        del request.session['patient_name']
    return redirect('login')


def login_required(function):
    def wrap(request, *args, **kwargs):
        if 'patient_id' not in request.session:
            return redirect('login')  # Cambia 'login' por la URL de inicio de sesión
        return function(request, *args, **kwargs)
    return wrap


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')



def buscar_medicos(request):
    specialization = Specialization.objects.all()
    medicos = Doctor.objects.all()

    specialization_id = request.GET.get('specialization')
    if specialization_id:
        medicos = medicos.filter(specialization_id=specialization_id)

    context = {
        'specializations': specialization,
        'doctors': medicos
    }
    return render(request, 'buscar_medicos.html', context)


@login_required
def reservar_cita(request, medico_id):
    doctor = get_object_or_404(Doctor, id=medico_id)
    patient_id = request.session.get('patient_id')
    paciente = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        fecha_hora = request.POST.get('fecha_hora')
        date_time = parse_datetime(fecha_hora)

        if is_time_available(doctor.schedule, date_time):
            cita = Appointment(doctor=doctor, patient=paciente, date_time=date_time)
            cita.save()
            return redirect('historial_citas')
        else:
            return render(request, 'reservar_cita.html', {
                'doctor': doctor,
                'error_message': 'El doctor no está disponible en la fecha y hora seleccionada.',
                'available_schedules': format_schedules(doctor.schedule)
            })

    available_schedules = format_schedules(doctor.schedule)
    return render(request, 'reservar_cita.html', {'doctor': doctor, 'available_schedules': available_schedules})

def is_time_available(schedule, date_time):
    day_name = date_time.strftime('%a')  # Ejemplo: 'Mon', 'Tue', etc.
    time = date_time.time()

    for days, hours in schedule.items():
        print(days, hours, "waaaa")
        if is_day_in_range(day_name, days):
            start, end = map(lambda t: datetime.strptime(t, '%H:%M').time(), hours)
            if start <= time <= end:
                return True
    return False

def is_day_in_range(day_name, days_range):
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    start_day, end_day = days_range.split(' - ')
    start_index = days_of_week.index(start_day)
    end_index = days_of_week.index(end_day)
    
    if start_index <= end_index:
        return day_name in days_of_week[start_index:end_index + 1]
    else:  # Caso para rangos como "Thu - Mon"
        return day_name in days_of_week[start_index:] + days_of_week[:end_index + 1]

def format_schedules(schedule):
    formatted_schedules = []
    for days, hours in schedule.items():
        start, end = hours
        formatted_schedules.append(f"{days}: {start} - {end}")
    return formatted_schedules


def ver_horarios(request, medico_id):
    doctor = get_object_or_404(Doctor, id=medico_id)
    schedule = doctor.schedule  # Asumiendo que esto es un JSON con los horarios

    context = {
        'doctor': doctor,
        'schedules': schedule
    }
    return render(request, 'ver_horarios.html', context)


@login_required
def historial_citas(request):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')

    context = {
        'appointments': appointments
    }
    return render(request, 'historial_citas.html', context)
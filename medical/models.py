from django.db import models

class Doctors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmada'),
        ('canceled', 'Cancelada'),
    ]

    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f'{self.doctor.name} - {self.patient.name} - {self.date_time}'

class Specializations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Users(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('patient', 'Paciente'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

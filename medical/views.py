from django.shortcuts import render, redirect
from .models import Specializations

# Create your views here.
def base(request):
    speci = Specializations.objects.all()
    return render(request, 'base.html', {'speci': speci})

def create_task(request):
    Specializations(name=request.POST['title'], description=request.POST['content']).save()
    return redirect('/test/')

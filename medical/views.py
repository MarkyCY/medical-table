from django.shortcuts import render

# Create your views here.
def list_test(request):
    return render(request, 'list_test.html')
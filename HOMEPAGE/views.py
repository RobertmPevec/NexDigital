from django.shortcuts import render

def home(request):
    return render(request, 'index.html')
def creator(request):
    return render(request, 'creator.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def login(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'register.html')
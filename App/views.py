from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Korisnik je uspješno registriran.")
            return redirect('home')
        else:
            messages.error(request, "Greška u unosu podataka. Pokušajte ponovno!")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {'form': form})
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django import forms
from .forms import RegistrationForm, LoginForm, DodajPredmet, DodajKorisnika, PromijeniLozinku
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Predmeti, Korisnik

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)

                if user.role == 'Stu':
                    return redirect('predmeti')
                elif user.role == 'Prof':
                    return redirect('home')
                elif user.role == 'Stu':
                    return redirect('home')
                else:
                    messages.error('Nemate pristup ovoj stranici!')
                    return redirect('login')
            else:
                messages.error("Netočno korisničko ime ili lozinka. Pokušajte ponovno!")
        else:
            messages.error(request, "Greška!")
    else:
        form = LoginForm()
    return render(request, "home-page/login.html", {'form': form})

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
    
    return render(request, "home-page/register.html", {'form': form})

def is_mentor(user):
    return user.is_authenticated and user.role == 'Stu'

def is_professor(user):
    return user.is_authenticated and user.role == 'Prof'

def is_student(user):
    return user.is_authenticated and user.role == 'Stu'

#admin stranica

#admin_predmeti
# @login_required
# @user_passes_test(is_mentor)
def admin_home_page(request):
    return render(request, 'admin-page/home_page.html')
def admin_predmeti(request):
    predmeti = Predmeti.objects.all()
    return render(request, 'admin-page/predmeti.html', {'predmeti' : predmeti})

def dodaj_predmet(request):

    if request.method == 'POST':
        form = DodajPredmet(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'predmeti')
        
    else:
        form = DodajPredmet()

    return render(request, "admin-page/dodaj_predmet.html", {'form': form})

def uredi_predmet(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)

    if request.method == 'POST':
        form = DodajPredmet(request.POST, instance=predmet)

        if form.is_valid():
            form.save()
            return redirect('predmeti')
    
    else:
        form = DodajPredmet(instance=predmet)

    return render(request, 'admin-page/uredi_predmet.html', {'form': form})

def izbrisi_predmet(request, predmet_id):

    predmet = get_object_or_404(Predmeti, id=predmet_id)

    if request.method == 'POST':
        predmet.delete()
        return redirect('predmeti')
    
    return render(request, 'admin-page/izbrisi_predmet.html', {'predmet': predmet})
        
#admin_studenti

def lista_studenata(request):
    studenti = Korisnik.objects.filter(role='Stu')
    return render(request, 'admin-page/lista_studenata.html', {'studenti': studenti})

def dodaj_korisnika(request):

    if request.method == 'POST':
        form = DodajKorisnika(request.POST)

        if form.is_valid():
            form.save()
            return redirect('admin_home_page')
    
    else:
        form = DodajKorisnika()

    return render(request, 'admin-page/dodaj_korisnika.html', {'form': form})

def uredi_studenta(request, student_id):
    student = get_object_or_404(Korisnik, id=student_id)

    if request.method == 'POST':
        form = DodajKorisnika(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('lista_studenata')
    
    else:
        form = DodajKorisnika(instance=student)

    return render(request, 'admin-page/uredi_student.html', {'form': form, 'student': student})

def resetiraj_lozinku(request, korisnik_id):

    korisnik = get_object_or_404(Korisnik, id=korisnik_id)

    if request.method == 'POST':
        form = PromijeniLozinku(request.POST)

        if form.is_valid():
            nova_lozinka = form.cleaned_data['nova_lozinka']
            korisnik.set_password(nova_lozinka)
            korisnik.save()

            return redirect('lista_studenata')
    
    else:
        form = PromijeniLozinku()

    return render(request, 'admin-page/promijeni_lozinku.html', {'form' : form})

def izbrisi_studenta(request, student_id):
    student = get_object_or_404(Korisnik, id=student_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            student.delete()
            return redirect('lista_studenata')
        elif 'cancel' in request.POST:
            return redirect('lista_studenata')

    return render(request, 'admin-page/izbrisi_studenta.html', {'student': student})

#admin_profesori

def lista_profesora(request):
    profesori = Korisnik.objects.filter(role='Prof')
    return render(request, 'admin-page/lista_profesora.html', {'profesori': profesori})

def uredi_profesora(request, profesor_id):

    profesor = get_object_or_404(Korisnik, id=profesor_id)

    if request.method == 'POST':
        form = DodajKorisnika(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('lista_profesora')
    
    else:
        form = DodajKorisnika(instance=profesor)

    return render(request, 'admin-page/uredi_profesora.html', {'form': form, 'profesor': profesor})

def izbrisi_profesora(request, profesor_id):
    profesor = get_object_or_404(Korisnik, id=profesor_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            profesor.delete()
            return redirect('lista_profesora')
        elif 'cancel' in request.POST:
            return redirect('lista_profesora')
        
    return render(request, 'admin-page/izbrisi_profesora.html', {'profesor': profesor})
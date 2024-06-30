from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django import forms
from .forms import RegistrationForm, LoginForm, DodajPredmet, DodajKorisnika, PromijeniLozinku, UpisForma
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Predmeti, Korisnik, Upis
from django.http import JsonResponse

def home(request):
    return render(request, 'home-page/home.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)

                if user.role == 'Stu':
                    student_id = user.id  
                    return redirect(reverse('upisni_list', kwargs={'student_id': student_id}))
                elif user.role == 'Prof':
                    return redirect(reverse('popis_predmeta_profesor', kwargs={'profesor_id': user.id}))
                elif user.role == 'Men':
                    return redirect(reverse('admin_home_page'))
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

def is_student_or_mentor(user):
    return user.is_authenticated and (user.role == 'Stu' or user.role == 'Men')

def student_or_mentor_required(view_func):
    actual_decorator = user_passes_test(is_student_or_mentor)
    return actual_decorator(view_func)

def is_mentor(user):
    return user.is_authenticated and user.role == 'Men'

def is_professor(user):
    return user.is_authenticated and user.role == 'Prof'

def is_student(user):
    return user.is_authenticated and user.role == 'Stu'

#admin stranica

#admin_predmeti
@login_required
@user_passes_test(is_mentor)
def admin_home_page(request):
    return render(request, 'admin-page/home_page.html')

@login_required
@user_passes_test(is_mentor)
def admin_predmeti(request):
    predmeti = Predmeti.objects.all()
    return render(request, 'admin-page/predmeti.html', {'predmeti' : predmeti})

@login_required
@user_passes_test(is_mentor)
def dodaj_predmet(request):

    if request.method == 'POST':
        form = DodajPredmet(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'predmeti')
        
    else:
        form = DodajPredmet()

    return render(request, "admin-page/dodaj_predmet.html", {'form': form})

@login_required
@user_passes_test(is_mentor)
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

@login_required
@user_passes_test(is_mentor)
def izbrisi_predmet(request, predmet_id):

    predmet = get_object_or_404(Predmeti, id=predmet_id)

    if request.method == 'POST':
        predmet.delete()
        return redirect('predmeti')
    
    return render(request, 'admin-page/izbrisi_predmet.html', {'predmet': predmet})

@login_required
@user_passes_test(is_mentor)
def popis_studenata(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisani_studenti = Upis.objects.filter(predmet=predmet, status='Enr')

    return render(request, 'admin-page/popis_studenata_predmeti.html', {'predmet': predmet, 'upisani_studenti': upisani_studenti})

        
#admin_studenti

@login_required
@user_passes_test(is_mentor)
def lista_studenata(request):
    studenti = Korisnik.objects.filter(role='Stu')
    return render(request, 'admin-page/lista_studenata.html', {'studenti': studenti})

@login_required
@user_passes_test(is_mentor)
def dodaj_korisnika(request):

    if request.method == 'POST':
        form = DodajKorisnika(request.POST)

        if form.is_valid():
            form.save()
            return redirect('admin_home_page')
    
    else:
        form = DodajKorisnika()

    return render(request, 'admin-page/dodaj_korisnika.html', {'form': form})

@login_required
@user_passes_test(is_mentor)
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

@login_required
@user_passes_test(is_mentor)
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

@login_required
@user_passes_test(is_mentor)
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

@login_required
@user_passes_test(is_mentor)
def lista_profesora(request):
    profesori = Korisnik.objects.filter(role='Prof')
    return render(request, 'admin-page/lista_profesora.html', {'profesori': profesori})

@login_required
@user_passes_test(is_mentor)
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

@login_required
@user_passes_test(is_mentor)
def izbrisi_profesora(request, profesor_id):

    profesor = get_object_or_404(Korisnik, id=profesor_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            profesor.delete()
            return redirect('lista_profesora')
        elif 'cancel' in request.POST:
            return redirect('lista_profesora')
        
    return render(request, 'admin-page/izbrisi_profesora.html', {'profesor': profesor})

#student stranica
@login_required
# @user_passes_test(is_student)
@student_or_mentor_required
def upisni_list(request, student_id):
    student = Korisnik.objects.get(id=student_id)
    upisani_predmeti = Upis.objects.filter(student=student)
    upisani_predmet_ids = upisani_predmeti.values_list('predmet_id', flat=True)
    neupisani_predmeti = Predmeti.objects.exclude(id__in=upisani_predmet_ids)

    predmeti_po_sem = {}
    for semestar in range(1, 9):
        if student.status == 'Red':
            predmeti_po_sem[semestar] = {
                'upisani': upisani_predmeti.filter(predmet__sem_red=semestar)
            }
        elif student.status == 'Izv':
            predmeti_po_sem[semestar] = {
                'upisani': upisani_predmeti.filter(predmet__sem_izv=semestar)
            }

    if request.method == 'POST':
        # Logika za upisivanje predmeta
        if 'upisi_predmet' in request.POST:
            predmet_id = request.POST['upisi_predmet']
            predmet = Predmeti.objects.get(id=predmet_id)
            Upis.objects.create(student=student, predmet=predmet, status='Enr')
            return redirect('upisni_list', student_id=student.id)
        
        # Logika za ažuriranje statusa predmeta (Položi/Ispiši)
        if 'update_status' in request.POST:
            upis_id = request.POST['update_status']
            upis = Upis.objects.get(id=upis_id)
            if upis.status == 'Enr':
                upis.status = 'Pass'
            elif upis.status == 'Pass':
                upis.status = 'Enr'
            upis.save()
            return redirect('upisni_list', student_id=student.id)
        
        # Logika za uklanjanje predmeta iz upisanih
        if 'remove_predmet' in request.POST:
            upis_id = request.POST['remove_predmet']
            Upis.objects.filter(id=upis_id).delete()
            return redirect('upisni_list', student_id=student.id)
    else:
        form = None  # Ne koristimo formu za dodavanje predmeta

    return render(request, 'student-page/upisni_list.html', {
        'form': form,
        'predmeti_po_sem': predmeti_po_sem,
        'neupisani_predmeti': neupisani_predmeti,
        'student': student,
    })


#profesor stranica

@login_required
@user_passes_test(is_professor)
def popis_predmeta_profesor(request, profesor_id):
    profesor = get_object_or_404(Korisnik, id=profesor_id)
    predmeti = Predmeti.objects.filter(nositelj=profesor_id)

    return render(request, 'profesor-page/popis_predmeta_profesor.html', {'predmeti' : predmeti, 'profesor' : profesor})

@login_required
@user_passes_test(is_professor)
def popis_studenata_predmet_profesor(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    upisani_studenti = Upis.objects.filter(predmet=predmet)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action:
            action_type, upis_id = action.split('-')
            upis = get_object_or_404(Upis, id=upis_id)
            
            if action_type == 'Passed':
                if upis.status != 'Fail':  
                    upis.status = 'Pass'
            elif action_type == 'Failed':
                upis.status = 'Fail'
            elif action_type == 'Enrolled':
                upis.status = 'Enr'
            
            upis.save()
            return redirect(reverse('popis_studenata_predmeti', kwargs={'predmet_id': predmet.id}))

    return render(request, 'profesor-page/popis_studenata_predmeti.html', {
        'predmet': predmet,
        'upisani_studenti': upisani_studenti
    })

@login_required
@user_passes_test(is_professor)
def students_lost_signature(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    studenti = Upis.objects.filter(predmet=predmet, status='Fail')
    return render(request, 'profesor-page/students_lost_signature.html', {
        'predmet': predmet,
        'studenti': studenti,
    })

@login_required
@user_passes_test(is_professor)
def students_got_signature(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    studenti = Upis.objects.filter(predmet=predmet, status='Enr')
    return render(request, 'profesor-page/students_got_signature.html', {
        'predmet': predmet,
        'studenti': studenti,
    })

@login_required
@user_passes_test(is_professor)
def students_passed(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    studenti = Upis.objects.filter(predmet=predmet, status='Pass')
    return render(request, 'profesor-page/students_passed.html', {
        'predmet': predmet,
        'studenti': studenti,
    })

"""
URL configuration for WebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/home/', views.home, name='home'),
    path('home-page/login/', views.login_view, name='login'),
    path('home-page/register/', views.registration, name='registration'),
    path('admin-page/home_page', views.admin_home_page, name='admin_home_page'),
    path('admin-page/predmeti/', views.admin_predmeti, name='predmeti'),
    path('admin-page/dodaj_predmet/', views.dodaj_predmet, name='dodaj_predmet'),
    path('admin-page/uredi_predmet/<int:predmet_id>/', views.uredi_predmet, name='uredi_predmet'),
    path('admin-page/izbrisi_predmet/<int:predmet_id>/', views.izbrisi_predmet, name='izbrisi_predmet'),
    path('admin-page/lista_studenata/', views.lista_studenata, name='lista_studenata'),
    path('admin-page/dodaj_korisnika/', views.dodaj_korisnika, name='dodaj_korisnika'),
    path('admin-page/uredi_studenta/<int:student_id>', views.uredi_studenta, name="uredi_studenta"),
    path('admin-page/promijeni_lozinku/<int:korisnik_id>', views.resetiraj_lozinku, name="resetiraj_lozinku"),
    path('admin-page/izbrisi_studenta/<int:student_id>', views.izbrisi_studenta, name='izbrisi_studenta'),
    path('admin-page/lista_profesora', views.lista_profesora, name='lista_profesora'),
    path('admin-page/uredi_profesor/<int:profesor_id>', views.uredi_profesora, name="uredi_profesora"),
    path('admin-page/izbrisi_profesora/<int:profesor_id>', views.izbrisi_profesora, name='izbrisi_profesora'),
]

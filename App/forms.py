from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import Korisnik, Predmeti, Upis
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Netočno korisničko ime ili lozinka!")
            
        return cleaned_data
    
class RegistrationForm(UserCreationForm):

    class Meta:
        model = Korisnik
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if Korisnik.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email {email} je već registriran.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Korisnik.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Username {username} već postoji.")
        return username
    
class DodajPredmet(ModelForm):
    
    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program', 'ects', 'sem_izv', 'sem_red', 'izborni', 'nositelj']

    def __init__(self, *args, **kwargs):
        super(DodajPredmet, self).__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = Korisnik.objects.filter(role='Prof')


class DodajKorisnika(ModelForm):

    class Meta:
        model = Korisnik
        fields = ['first_name', 'last_name', 'username', 'email', 'status', 'role', 'is_superuser']

class PromijeniLozinku(forms.Form):
    nova_lozinka = forms.CharField(widget=forms.PasswordInput)
    potvrda_lozinke = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        lozinka = cleaned_data.get("nova_lozinka")
        potvrda = cleaned_data.get("potvrda_lozinke")

        if lozinka != potvrda:
            raise forms.ValidationError("Lozinke se ne podudaraju!")
        
        return cleaned_data
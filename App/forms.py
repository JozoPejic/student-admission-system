from django import forms
from .models import Korisnik
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Obavezno. Upišite postojeću email adresu.")

    class Meta:
        model = Korisnik
        fields = ('email', 'username', 'password1')

        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            if Korisnik.objects.filter(email=email).exists():
                raise forms.ValidationError(f"Email {email} je već registriran.")
            return email
        
        def clean_username(self):
            username = self.cleaned_data['username']
            if Korisnik.objects.filter(username=username).exists():
                raise forms.ValidationError(f"Username {username} već postoji.")
            return username
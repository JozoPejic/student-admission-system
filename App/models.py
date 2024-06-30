from django.db import models
from django.contrib.auth.models import AbstractUser

class Korisnik(AbstractUser):
    STATUS = (('None', 'none'), ('Izv', 'izvanredan'), ('Red', 'redovan'))
    ROLES = (('Men', 'Mentor'), ('Stu', 'Student'), ('Prof', 'Profesor'))
    status = models.CharField(max_length=10, choices=STATUS, default='None')
    role = models.CharField(max_length=10, choices=ROLES, default='Stu')

class Predmeti(models.Model):
    name = models.CharField(max_length=100)
    kod = models.CharField(max_length=20)
    program = models.CharField(max_length=100)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(choices=[('Da', 'da'), ('Ne', 'ne')], max_length=10)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.kod})"

class Upis(models.Model):
    STATUS = (('Not', 'Not Enrolled'), ('Pass', 'Passed'), ('Enr', 'Enrolled'), ('Fail', 'Failed'))
    student = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default='Not') 

    def promijeni_status(self, novi_status):
        if novi_status in dict(self.STATUS):
            self.status = novi_status
            self.save()


from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import User

class Annonces(models.Model):
    title = models.CharField(max_length=255)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    #ens = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Formation(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE)  # L'enseignant qui a créé le cours

    def __str__(self):
        return self.titre

class Chapitre(models.Model):
    cours = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='chapitres')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    fichier = models.FileField(upload_to='learn/media/', blank=True, null=True)  # Champ pour le fichier


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='none@email.com')
    telephone = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(default='1975-12-12')


    def __str__(self):
        return self.user.username



class Devoir(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    fichier = models.FileField(upload_to='devoirs/', blank=True, null=True)
    date_depot = models.DateTimeField(auto_now_add=True)
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)  # Associe un étudiant à chaque devoir
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.titre


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)

    def _str_(self):
        return str(self.message)

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)  # Si un seul destinataire
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)



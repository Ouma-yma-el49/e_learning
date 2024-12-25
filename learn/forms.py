from django import forms
from .models import Annonces, Formation, Chapitre, Profile, Devoir, Webinaire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AnnoncesForm(forms.ModelForm):
    class Meta:
        model = Annonces
        fields = ['title', 'contenu']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'annonce'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu de l\'annonce'}),
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'description']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du cours'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du cours',

            }),
        }

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['titre', 'description', 'fichier']



# Formulaire pour le modèle User
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Corriger le modèle à `Profile`
        fields = ['first_name', 'last_name', 'email', 'avatar', 'telephone', 'date_naissance']  # Ajouter les champs nécessaires

    avatar = forms.ImageField(required=False)  # Autoriser l'upload d'une image sans en faire un champ obligatoire
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','last_name','first_name']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DevoirForm(forms.ModelForm):
    class Meta:
        model = Devoir
        fields = ['titre', 'description', 'fichier']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Devoir
        fields = ['note']
        labels = {
            'note': 'Attribuer une note',
        }
        widgets = {
            'note': forms.NumberInput(attrs={'min': 0, 'max': 20, 'step': 0.5}),
        }

class MessageForm(forms.Form):
    subject = forms.CharField(max_length=100, label="Objet")
    message = forms.CharField(widget=forms.Textarea, label="Message")



class WebinaireForm(forms.ModelForm):
    class Meta:
        model = Webinaire
        fields = ['titre','lien']
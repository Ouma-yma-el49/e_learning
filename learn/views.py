from django.views.decorators.csrf import csrf_exempt
import json

from django.db.models.functions.datetime import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import AnnoncesForm, ChapitreForm, UserForm,DevoirForm,WebinaireForm
from .models import Formation, Chapitre, User, Devoir, Message, Annonces
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CoursForm
from django.core.validators import validate_email
from django.db.models import Q, Avg, Count, functions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from django.http import JsonResponse
from .models import Webinaire

def acceuil(request):
    return render(request, 'acceuil.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')

def contact(request):
    return render(request, 'contact.html')

def home_ens(request):
    total_etu = User.objects.filter(email__icontains='-etu@etu.univh2c.ma').count()
    total_cours = Formation.objects.count()
    total_webinaires = Webinaire.objects.count()
    total_devoirs = Devoir.objects.filter(note__isnull=True).count()  # Exemple
    moyenne_notes = round(Devoir.objects.aggregate(Avg('note'))['note__avg'] ,2)# Moyenne des notes des étudiants
    taux_reussite = round((Devoir.objects.filter(note__gte=10).count() / total_etu) * 10, 2) if total_etu > 0 else 0
    annonces = Annonces.objects.all().order_by('-date_creation')[:5]  # Dernières annonces
    # Données pour les graphiques

    # Obtenir les webinaires par mois
    # Webinaires par mois
    webinaire_par_mois = (
        Webinaire.objects.annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    labels_webinaires = [w['month'].strftime('%B %Y') for w in webinaire_par_mois]
    data_webinaires = [w['count'] for w in webinaire_par_mois]

    # Cours par mois
    cours_par_mois = Formation.objects.annotate(month=TruncMonth('date_creation')).values('month').annotate(
        count=Count('id')).order_by('month')
    labels_cours = [str(c['month'].strftime('%B %Y')) for c in cours_par_mois]
    data_cours = [c['count'] for c in cours_par_mois]

    # Étudiants inscrits par mois
    etudiants_par_mois = User.objects.filter(email__icontains='-etu@etu.univh2c.ma').annotate(month=TruncMonth('date_joined')).values(
        'month').annotate(count=Count('id')).order_by('month')
    labels_etudiants = [str(e['month'].strftime('%B %Y')) for e in etudiants_par_mois]
    data_etudiants = [e['count'] for e in etudiants_par_mois]


    context = {
        'total_cours': total_cours,
        'total_etu': total_etu,
        'total_webinaires': total_webinaires,
        'total_devoirs': total_devoirs,
        'moyenne_notes': moyenne_notes,
        'taux_reussite': taux_reussite,
        'annonces': annonces,
        'labels_webinaires': labels_webinaires,
        'data_webinaires': data_webinaires,
        'labels_cours': labels_cours,
        'data_cours': data_cours,
        'labels_etudiants': labels_etudiants,
        'data_etudiants': data_etudiants,
    }
    return render(request, 'dashboard/enseignant/home.html', context)
def home_etu(request):
    annonces = Annonces.objects.all().values()
    context = {
        'annonces': annonces,
    }

    return render(request, 'dashboard/etudiant/home_etu.html',context)
def annonce(request):
    annonces = Annonces.objects.all().values().order_by('-date_creation')
    context = {
        'annonces': annonces,
    }
    return render(request, 'dashboard/etudiant/annonces.html',context)

def annonces_list(request):
    annonces = Annonces.objects.all().values().order_by('-date_creation')
    return render(request,'dashboard/enseignant/Annonces/annonce_list.html',{'annonces':annonces,})


def add_annonces(request):
    if request.method == 'POST':
        form = AnnoncesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('annonces_list')
    else:
        form = AnnoncesForm()
        return render(request, 'dashboard/enseignant/Annonces/add_annonce.html', {'form': form})


def edit_annonce(request, id):
    annonce = get_object_or_404(Annonces, id=id)  # Récupère l'annonce ou renvoie 404 si non trouvée
    # if request.method == 'POST':
    form = AnnoncesForm(request.POST, instance=annonce)
    if form.is_valid():
        form.save()  # Enregistre les modifications
        return redirect('annonces_list')  # Redirige vers la liste des annonces (ajustez l'URL selon votre nom)
    else:
        form = AnnoncesForm(instance=annonce)  # Pré-remplit le formulaire avec les données existantes
    return render(request, 'dashboard/enseignant/Annonces/edit_annonce.html', {'form': form, 'annonce': annonce})

def delete_annonce(request, id):
    annonce = get_object_or_404(Annonces, id=id)  # Récupère l'annonce ou renvoie 404 si elle n'existe pas
    annonce.delete()  # Supprime l'annonce directement
    return redirect('annonces_list')  # Redirige vers la liste des annonces (ajustez le nom d'URL selon votre projet)
from django.views.decorators.csrf import csrf_exempt
@login_required
@csrf_exempt
def profil_utilisateur(request):
    if request.method == 'POST':
        user = request.user
        user.last_name = request.POST.get('last_name', user.last_name)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)
        user.save()
        return JsonResponse({'success': True})
    return render(request, 'dashboard/enseignant/profil.html', {'user': request.user})
@login_required
def liste_cours(request):
    cours = Formation.objects.all()  # Affiche tous les cours
    return render(request, 'dashboard/enseignant/Gestion_cours/list_cours.html', {'cours': cours})


def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST, request.FILES)
        if form.is_valid():
            # Créez l'instance de Cours sans l'enregistrer encore
            cours = form.save(commit=False)
            cours.enseignant = request.user  # Associez l'enseignant connecté
            cours.save()  # Enregistrez le cours
            return redirect('cours_list')  # Redirige vers les détails du cours
    else:
        form = CoursForm()

    return render(request, 'dashboard/enseignant/Gestion_cours/ajouter_cours.html', {'form': form})



def modifier_cours(request, cours_id):
    cours = Formation.objects.get(id=cours_id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')

        # Mise à jour des champs
        if titre:
            cours.titre = titre
        if description:
            cours.description = description

        # Sauvegarde dans la base de données
        cours.save()

        # Redirection vers la page des cours
        return redirect('cours_list')  # Nom de l'URL de votre page affichant les cours

    return redirect('cours_list')

def supprimer_cours(request, pk):
    cours = get_object_or_404(Formation, pk=pk)  # Obtenez le cours par son ID
    cours.delete()  # Supprimez le cours
    return redirect('cours_list')

def ajouter_chapitre(request, cours_id):
    cours = get_object_or_404(Formation, id=cours_id)
    if request.method == 'POST':
        form = ChapitreForm(request.POST, request.FILES)  # N'oubliez pas d'ajouter request.FILES ici
        if form.is_valid():
            chapitre = form.save(commit=False)  # Ne pas encore sauvegarder l'objet
            chapitre.cours = cours  # Associer le chapitre au cours
            chapitre.save()  # Sauvegarder l'objet maintenant
            return redirect('detail_cours', cours_id=cours.id)
    else:
        form = ChapitreForm()
    return render(request, 'dashboard/enseignant/Gestion_cours/ajouter_chapitre.html', {'form': form, 'cours': cours})

def detail_cours(request, cours_id):
    # Récupérer le cours par son ID
    cours = get_object_or_404(Formation, id=cours_id)
    # Récupérer tous les chapitres associés à ce cours
    chapitres = cours.chapitres.all()
    # Récupérer tous les quizzes associés à ce cours

    context = {
        'cours': cours,
        'chapitres': chapitres,

    }
    return render(request, 'dashboard/enseignant/Gestion_cours/detail_cours.html', context)


def modifier_chapitre(request, pk):
    chapitre = get_object_or_404(Chapitre, pk=pk)
    cours = chapitre.cours  # Récupérer le cours associé au chapitre

    if request.method == 'POST':
        form = ChapitreForm(request.POST, request.FILES, instance=chapitre)  # Passer request.FILES pour gérer les fichiers
        if form.is_valid():
            # Si un nouveau fichier a été téléchargé, le mettre à jour
            if 'nouveau_fichier' in request.FILES:
                chapitre.fichier = request.FILES['nouveau_fichier']  # Mettre à jour le fichier
            form.save()  # Sauvegarder les autres modifications (titre, description, etc.)
            return redirect('detail_cours', cours_id=cours.id)  # Rediriger vers la page du cours associé

    else:
        form = ChapitreForm(instance=chapitre)  # Si c'est une requête GET, afficher le formulaire avec les données du chapitre existant

    return render(request, 'dashboard/enseignant/Gestion_cours/edit_chapitre.html', {'form': form, 'chapitre': chapitre, 'cours': cours})

def supprimer_chapitre(request, pk):
    chapitre = get_object_or_404(Chapitre, pk=pk)  # Obtenez le cours par son ID
    chapitre.delete()  # Supprimez le cours
    return redirect('cours_list')


def sing_in(request):
    error = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Vérifier si l'utilisateur existe avec cet email
        user = User.objects.filter(email=email).first()
        if user:
            # Authentifier l'utilisateur en utilisant son nom d'utilisateur et son mot de passe
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                # Connexion réussie
                login(request, auth_user)
                # Vérifier si l'email contient @ens.ma
                if email.endswith('-etu@etu.univh2c.ma'): # mail universitaire pour etudiant
                    return redirect('home_etu')  # Redirige vers la page d'accueil
                else:
                    if email.endswith('@ens.ma'):
                        return redirect('dashboard')
                    else :
                        error = True
                        message=("Impossible de vous se connecter. "
                                 "Vous devriez vous s'inscrire avec un indicatif universitaire")
            else:
                # Mot de passe incorrect
                error = True
                message = "Mot de passe incorrect"
        else:
            # Utilisateur non trouvé
            error = True
            message = "L'utilisateur n'existe pas"

    context = {
        'error': error,
        'message': message}

    # Rendre la page avec le contexte approprié
    return render(request, 'login.html', context)

def sing_up(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirmpassword = request.POST.get('confirmpassword', None)
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != confirmpassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"

        # register
        if error == False:
            user = User(
                username=name,
                email=email,
            )
            user.save()

            user.password = password
            user.set_password(user.password)
            user.save()

            return redirect('sing_in')


    context = {
        'error': error,
        'message': message
    }
    return render(request, 'register.html', context)


def log_out(request):
    logout(request)
    return redirect('sing_in')


def liste_etudiants(request):
    etudiants = User.objects.filter(email__icontains='-etu@etu.univh2c.ma')
    context = {
        'etudiants': etudiants,
    }
    return render(request, 'dashboard/enseignant/Gestion_etu/liste_etu.html', context)


def delete_etu(request, user_id):
    etudiant = get_object_or_404(User, id=user_id)
    etudiant.delete()  # Supprimer l'étudiant
    return redirect('liste_etudiants')  # Rediriger vers la liste des étudiants


def add_etudiant(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde le nouvel étudiant
            return redirect('liste_etudiants')  # Redirige vers la liste des étudiants
    else:
        form = UserForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/enseignant/Gestion_etu/add_etu.html', context)


def cours(request):
    cours = Formation.objects.all()  # Affiche tous les cours
    return render(request, 'dashboard/etudiant/cours.html', {'cours': cours})

def detail_cours_etu(request, cours_id):
    # Récupérer le cours par son ID
    cours = get_object_or_404(Formation, id=cours_id)
    # Récupérer tous les chapitres associés à ce cours
    chapitres = cours.chapitres.all()
    # Récupérer tous les quizzes associés à ce cours
# Assurez-vous que votre modèle Formation a une relation avec les quizzes

    context = {
        'cours': cours,
        'chapitres': chapitres,

    }
    return render(request, 'dashboard/etudiant/detail_cours.html', context)



def telecharger_fichier(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)

    # Vérifie si le chapitre a un fichier
    if chapitre.fichier:
        # Retourne le fichier en réponse HTTP
        response = FileResponse(chapitre.fichier.open(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{chapitre.fichier.name}"'
        return response
    else:
        # Si aucun fichier n'est associé, vous pouvez renvoyer une erreur ou un message
        return HttpResponse("Aucun fichier disponible pour ce chapitre.", status=404)


@login_required
@login_required
def gestion_devoirs(request):
    devoir_id = request.GET.get("devoir_id")

    # Filtrer les devoirs pour afficher uniquement ceux ajoutés par l'étudiant connecté
    devoirs = Devoir.objects.filter(etudiant=request.user)  # Afficher seulement les devoirs de l'étudiant connecté

    selected_devoir = None

    if devoir_id:
        selected_devoir = get_object_or_404(Devoir, id=devoir_id)
        form = DevoirForm(request.POST or None, request.FILES or None, instance=selected_devoir)
    else:
        form = DevoirForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        devoir = form.save(commit=False)
        devoir.etudiant = request.user  # Associe l'étudiant connecté au devoir
        devoir.save()
        return redirect('devoirs')  # Rediriger vers la page des devoirs après l'ajout

    context = {
        'devoirs': devoirs,
        'form': form,
        'selected_devoir': selected_devoir,
    }
    return render(request, 'dashboard/etudiant/gestion_devoirs.html', context)


@login_required
def edit_devoir(request, devoir_id):
    devoir = get_object_or_404(Devoir, id=devoir_id)

    # Vérifie que l'étudiant connecté est bien celui qui a soumis le devoir
    if devoir.etudiant != request.user:
        return redirect('devoirs')  # Rediriger vers la page des devoirs si l'étudiant essaie d'éditer un devoir qui ne lui appartient pas

    if request.method == 'POST':
        form = DevoirForm(request.POST, request.FILES, instance=devoir)
        if form.is_valid():
            form.save()
            return redirect('devoirs')  # Rediriger vers la page des devoirs après l'édition
    else:
        form = DevoirForm(instance=devoir)

    return render(request, 'dashboard/etudiant/gestion_devoirs.html', {'form': form, 'devoir': devoir})

# Fonction de vérification pour s'assurer que seul un enseignant peut accéder à la vue
def est_enseignant(user):
    return user.email.endswith('@ens.ma')

@login_required
@user_passes_test(est_enseignant)
def visualiser_devoirs_enseignant(request):
    # Récupère tous les devoirs déposés par les étudiants
    devoirs = Devoir.objects.select_related('etudiant').order_by('-date_depot')

    # Context pour passer les devoirs à la template
    return render(request, 'dashboard/enseignant/visualiser_devoirs.html', {
        'devoirs': devoirs,
    })


# Vue pour noter un devoir
@login_required
@user_passes_test(est_enseignant)
def noter_devoir(request, devoir_id):
    devoir = get_object_or_404(Devoir, id=devoir_id)

    if request.method == 'POST':
        note = request.POST.get('note')
        if note:
            devoir.note = note
            devoir.save()

    return redirect('visualiser_devoirs')  # Redirige vers la page des devoirs


def delete_devoir(request, pk):
    devoir = get_object_or_404(Devoir, id=pk)
    devoir.delete()  # Supprimer le devoir
    return redirect('devoirs')  # Rediriger vers la page des devoirs

@login_required
def chat(request):
    messages = Message.objects.all().order_by('-created_at')  # Obtenez tous les messages
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Définir 'to_user' ici - vous devez probablement définir un utilisateur spécifique
            to_user = User.objects.first()  # Par exemple, récupérer un utilisateur par défaut, ou gérer un chat de groupe
            Message.objects.create(from_user=request.user, to_user=to_user, content=content, timestamp=timezone.now())
            return redirect('chat')  # Assurez-vous que le nom de l'URL est correct
    return render(request, 'dashboard/etudiant/group_chat.html', {'messages': messages})

@login_required
def chat_enseignant(request):
    messages = Message.objects.all().order_by('-created_at')  # Obtenez tous les messages
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Définir 'to_user' ici pour définir un utilisateur spécifique
            to_user = User.objects.first()  # Par exemple, récupérer un utilisateur par défaut, ou gérer un chat de groupe
            Message.objects.create(from_user=request.user, to_user=to_user, content=content, timestamp=timezone.now())
            return redirect('chat_enseignant')  # Assurez-vous que le nom de l'URL est correct
    return render(request, 'dashboard/enseignant/Gestion_etu/chat.html', {'messages': messages})

@login_required
def profile_view(request):

    # Passer les données de l'utilisateur au template
    context = {
        'user': request.user
    }
    return render(request, 'dashboard/etudiant/profil.html', context)

def update_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Rediriger vers la page de profil après la mise à jour
    else:
        form = UserForm(instance=request.user)

    return render(request, 'dashboard/etudiant/profil.html', {'form': form})



# Afficher la liste des webinaires et gérer l'ajout et la suppression
def gestion_webinaires(request):
    # Récupérer tous les webinaires non terminés
    webinaires = Webinaire.objects.all().order_by("-date_creation")
    context = {
        'webinaires': webinaires,
    }
    return render(request, 'dashboard/enseignant/gestion_webinaires.html', context)
# Ajouter un webinaire
def ajouter_webinaire(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        date= request.POST.get('date')
        lien = request.POST.get('lien')
        webinaire = Webinaire.objects.create(titre=titre, date=date, lien=lien, enseignant=request.user )
        return redirect('gestion_webinaires')

# Supprimer un webinaire
def supprimer_webinaire(request, id):
    webinaire = Webinaire.objects.get(id=id)
    webinaire.delete()
    return redirect('gestion_webinaires')

@login_required
def webinaires_etudiant(request):
    # Filtrer les webinaires par disponibilité ou critères spécifiques
    webinaires = Webinaire.objects.filter().order_by('-date_creation')

    context = {
        'webinaires': webinaires,  # Passer la liste des webinaires au template
    }

    return render(request, 'dashboard/etudiant/webinaire_liste.html', context)


def signaler_termine(request, webinaire_id):
    webinaire = Webinaire.objects.get(id=webinaire_id)
    webinaire.est_termine= True
    webinaire.save()
    return redirect('gestion_webinaires')  # Redirige vers la page des webinaires

@csrf_exempt
def update_webinaire_state(request):
    if request.method == "POST":
        data = json.loads(request.body)
        webinaire_id = data.get('webinaire_id')
        new_state = data.get('etat')

        # Vérifier que l'état est valide
        if new_state not in dict(Webinaire.STATUT_CHOICES):
            return JsonResponse({'success': False, 'error': 'État invalide.'})

        try:
            webinaire = Webinaire.objects.get(id=webinaire_id)
            # Mise à jour de l'état
            webinaire.etat = new_state
            webinaire.save()

            return JsonResponse({'success': True})
        except Webinaire.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Webinaire introuvable.'})

    return JsonResponse({'success': False, 'error': 'Requête invalide.'})
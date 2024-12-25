from tkinter.font import names

from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [

# Shared URLs
        path('', views.acceuil, name='acceuil'),
        path('login/', views.sing_in, name='sing_in'),
        path('register', views.sing_up, name='sing_up'),
        path('logout/', views.log_out, name='log_out'),
        path('about/', views.about, name='about'),
        path('services/', views.services, name='services'),
        path('contact/', views.contact, name='contact'),
        path('dashboard/', views.home_ens, name='dashboard'),
        path('home_etu/', views.home_etu, name='home_etu'),

        path('annonces/', views.annonces_list, name='annonces_list'),
        path('annonces/add/', views.add_annonces, name='add_annonces'),
        path('dashboard/enseignant/profil/', views.profil_utilisateur, name='profil_utilisateur'),
        path('annonces/<int:id>/edit/', views.edit_annonce, name='edit_annonce'),
        path('annonces/<int:id>/delete/', views.delete_annonce, name='delete_annonce'),
        path('gestion_cours/', views.liste_cours, name='cours_list'),
        path('gestion_cours/ajouter/', views.ajouter_cours, name='ajouter_cours'),  # Correction ici
        path('gestion_cours/modifier/<int:cours_id>/', views.modifier_cours, name='modifier_cours'),  # Correction ici
        path('gestion_cours/supprimer/<int:pk>/', views.supprimer_cours, name='supprimer_cours'),
        path('cours/<int:cours_id>/ajouter_chapitre/', views.ajouter_chapitre, name='ajouter_chapitre'),
        path('<int:cours_id>/', views.detail_cours, name='detail_cours'),
        path('cours/chapitre/modifier/<int:pk>/', views.modifier_chapitre, name='edit_chapitre'),
        path('cours/chapitre/supprimer/<int:pk>/', views.supprimer_chapitre, name='delete_chapitre'),

        path('Gestion_etu/etudiants/', views.liste_etudiants, name='liste_etudiants'),
        path('Gestion_etu/etudiants/ajouter/', views.add_etudiant, name='add_etudiant'),

         path('Gestion_etu/etudiants/delete/<int:user_id>/', views.delete_etu, name='delete_etu'),
        path('dashboard/etudiant/mescours',views.cours, name='mescours'),
        path('dashboard/etudiant/mescours/<int:cours_id>/', views.detail_cours_etu, name='detail_cours_etu'),

        path('telecharger_fichier/<int:chapitre_id>/', views.telecharger_fichier, name='telecharger_fichier'),
        path('dashboard/enseignant/devoirs/', views.visualiser_devoirs_enseignant, name='visualiser_devoirs'),
        path('dashboard/enseignant/devoirs/<int:devoir_id>/noter/', views.noter_devoir, name='noter_devoir'),
        path('dashboard/etudiant/devoirs/', views.gestion_devoirs, name='devoirs'),
        path('dashboard/etudiant/devoirs/edit_devoir/<int:devoir_id>/', views.edit_devoir, name='edit_devoir'),
        path('dashboard/etudiant/devoir/<int:pk>/supprimer/', views.delete_devoir, name='delete_devoir'),
        path('dashboard/etudiant/annonces', views.annonce, name='annonce'),
        path('dashboard/etudiant/chat', views.chat, name='chat'),
        path('chat/', views.chat_enseignant, name='chat_enseignant'),
        path('profile/', views.profile_view, name='profile'),
        path('profile/update', views.update_profile, name='update_profile'),
        path('gestion_webinaires/', views.gestion_webinaires, name='gestion_webinaires'),
        path('ajouter_webinaire/', views.ajouter_webinaire, name='ajouter_webinaire'),
        path('supprimer_webinaire/<int:id>/', views.supprimer_webinaire, name='supprimer_webinaire'),
        path('webinaires/', views.webinaires_etudiant, name='webinaires_etudiant'),
        path('signaler_termine/<int:webinaire_id>/', views.signaler_termine, name='signaler_termine'),
        path('update_webinaire_state/', views.update_webinaire_state, name='update_webinaire_state'),




]
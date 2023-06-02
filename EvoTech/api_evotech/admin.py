from django.contrib import admin

# Register your models here.
from .models import *
class MeteoAdmin(admin.ModelAdmin):
    list = ('idMeteo', 'Temperature', 'prevision')

    admin.site.register(Meteo)


class ThemeAdmin(admin.ModelAdmin):
    list = ('idTheme', 'labelT')

    admin.site.register(Theme)

class CategorieAdmin(admin.ModelAdmin):
    list = ('idCategorie', 'labelC')

    admin.site.register(Categorie)

class UserAdmin(admin.ModelAdmin):
    list = ('idUser', 'nomUser', 'prenomUser', 'username', 'motdepasse', 'profile')

    admin.site.register(User)

class RegionAdmin(admin.ModelAdmin):
    list = ('numRegion', 'nomRegion', 'adminRegion')

    admin.site.register(Region)

class VilleAdmin(admin.ModelAdmin):
    list = ('idVille', 'nomVille', 'regionV')

    admin.site.register(Ville)

class LieuAdmin(admin.ModelAdmin):
    list = ('idLieu', 'nomLieu', 'descripLieu', 'exigence', 'faitHisto', 'produitArtis',
            'expressCourantes', 'longitude', 'latitude', 'H_ouverture', 'H_fermeture', 'climat','region',
             'adminRegion','feedback' ,'nmb_feedbach')

    admin.site.register(Lieu)

class MoyenTransportAdmin(admin.ModelAdmin):
    list = ('idTransport', 'typeTrans')

    admin.site.register(MoyenTransport)

class TransportAdmin(admin.ModelAdmin):
    list = ('id_trans', 'id_moytrans', 'id_lieu', 'H_depart')

    admin.site.register(Transport)

class EvenementAdmin(admin.ModelAdmin):
    list = ('idEvent', 'nomEvent', 'descripEvent', 'dateEvent', 'H_debut', 'H_fin','lieu')

    admin.site.register(Evenement)
class CommentAdmin(admin.ModelAdmin):
    list = ('lieu', 'author', 'text', 'created_at')

    admin.site.register(Comment)

class NotificationAdmin(admin.ModelAdmin):
    list = ('adminreg', 'author', 'lieu', 'created_at','is_read')

    admin.site.register(Notification)   

class FeedbackAdmin(admin.ModelAdmin):
    list = ('user', 'lieu', 'rating', )

    admin.site.register(Feedback) 

"""class LocalEventAdmin(admin.ModelAdmin):
    list = ('id_localEvent', 'id_event', 'id_lieu')

    admin.site.register(LocalEvent)"""

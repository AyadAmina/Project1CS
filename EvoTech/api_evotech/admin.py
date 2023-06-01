from django.contrib import admin

# Register your models here.
from .models import *
class MeteoAdmin(admin.ModelAdmin):
    list = ('idMeteo', 'Temperature', 'prevision')

    admin.site.register(Meteo)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photoId', 'image', 'lieuId', 'eventId')

    admin.site.register(Photo)

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

class CommuneAdmin(admin.ModelAdmin):
    list = ('idCommune', 'nomCommune', 'regionC')

    admin.site.register(Commune)


class LieuAdmin(admin.ModelAdmin):
    list = ('idLieu', 'nomLieu', 'descripLieu', 'exigence', 'faitHisto', 'produitArtis',
            'expressCourantes', 'longitude', 'latitude', 'H_ouverture', 'H_fermeture', 'climat','region',
             'adminRegion', 'id_event' )

    admin.site.register(Lieu)


class TransportAdmin(admin.ModelAdmin):
    list = ('id_trans', 'typeTrans', 'id_lieu')

    admin.site.register(Transport)

class EvenementAdmin(admin.ModelAdmin):
    list = ('idEvent', 'nomEvent', 'descripEvent', 'dateEvent', 'H_debut', 'H_fin')

    admin.site.register(Evenement)

"""class LocalEventAdmin(admin.ModelAdmin):
    list = ('id_localEvent', 'id_event', 'id_lieu')

    admin.site.register(LocalEvent)"""

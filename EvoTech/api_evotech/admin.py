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

class CommuneAdmin(admin.ModelAdmin):
    list = ('idComm', 'nomComm', 'regionC')

    admin.site.register(Commune)

class LieuAdmin(admin.ModelAdmin):
    list = ('idLieu', 'nomLieu', 'descripLieu', 'exigence', 'faitHisto', 'produitArtis',
            'expressCourantes', 'longitude', 'latitude', 'H_ouverture', 'H_fermeture', 'climat','region',
             'commune','categorie','theme','transport' )

    admin.site.register(Lieu)

class TransportAdmin(admin.ModelAdmin):
    list = ('idTransport', 'typeTrans')

    admin.site.register(Transport)


class EvenementAdmin(admin.ModelAdmin):
    list = ('idEvent', 'nomEvent', 'descripEvent', 'dateEvent', 'H_debut', 'H_fin','id_lieu')

    admin.site.register(Evenement)

class PhotoAdmin(admin.ModelAdmin):
    list = ('photoId', 'image', 'lieuId', 'eventId')

    admin.site.register(Photo)

class FavorisAdmin(admin.ModelAdmin):
    list = (' id_favoris', 'idUser', 'id_lieu')

    admin.site.register(Favoris)

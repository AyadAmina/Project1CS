from django.db import models

# Create your models here.
class Meteo(models.Model):
    idMeteo = models.AutoField(primary_key=True)
    Temperature = models.IntegerField()
    prevision = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return (str(self.idMeteo))
    

class Theme(models.Model):
   idTheme = models.AutoField(primary_key=True)
   labelT = models.CharField(max_length=100)

   def __str__(self) -> str:
        return (self.labelT)

class Categorie(models.Model):
   idCategorie = models.AutoField(primary_key=True)
   labelC = models.CharField(max_length=100, default='')

   def __str__(self) -> str:
        return (self.labelC)

class User(models.Model):
   idUser = models.AutoField(primary_key=True)
   nomUser = models.CharField(max_length=100)
   prenomUser = models.CharField(max_length=100)
   username = models.CharField(max_length=100)
   motdepasse = models.CharField(max_length=100)
   profile = models.CharField(max_length=100)#capable ytbdl ça dépend la fonctionnalitée kifch ttkhdam

   def __str__(self) -> str:
        return (self.username)

class Region(models.Model):
   numRegion = models.AutoField(primary_key=True)
   nomRegion = models.CharField(max_length=100)
   adminRegion = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   def __str__(self) -> str:
        return (self.nomRegion)

class Commune(models.Model):
   idComm = models.AutoField(primary_key=True)
   nomComm = models.CharField(max_length=100)
   regionC = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
   def __str__(self) -> str:
        return (self.nomComm)
   
class Transport(models.Model):
   idTransport = models.AutoField(primary_key=True)
   typeTrans = models.CharField(max_length=100, default="")
   def __str__(self) -> str:
        return (str(self.typeTrans))


   
class Lieu(models.Model):
    idLieu = models.AutoField(primary_key=True)
    nomLieu = models.CharField(max_length=100)
    descripLieu = models.CharField(max_length=1000, blank=True)
    exigence = models.CharField(max_length=1000, blank=True)
    faitHisto = models.CharField(max_length=1000, blank=True)
    produitArtis = models.CharField(max_length=1000, default="", blank=True)
    expressCourantes = models.CharField(max_length=1000, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    H_ouverture = models.TimeField(blank=True, null=True)
    H_fermeture = models.TimeField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,blank=True, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True,  blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)
    transport = models.ManyToManyField(Transport, null=True, blank=True)
    def __str__(self) -> str:
        return self.nomLieu   
    
class Evenement(models.Model):
   idEvent = models.AutoField(primary_key=True)
   nomEvent = models.CharField(max_length=100)
   descripEvent = models.CharField(max_length=1000)
   dateEvent = models.DateField()
   H_debut = models.TimeField()
   H_fin = models.TimeField()
   id_lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, null=True, blank=True)
   def __str__(self) -> str:
        return (str(self.nomEvent))

class Photo(models.Model):
    photoId = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='static/images', default = '')
    lieuId= models.ForeignKey(Lieu, on_delete=models.CASCADE , null=True, related_name='photos', blank=True)
    eventId = models.ForeignKey(Evenement, on_delete=models.CASCADE , null=True, related_name='images')

    def __str__(self) -> str:
          return (str(self.image))


from django.db import models
# Create your models here.
class Search(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

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
   profile = models.CharField(max_length=100)

   is_authenticated = models.BooleanField(default=False)

   def __str__(self) -> str:
        return (self.username)

class Region(models.Model):
   numRegion = models.AutoField(primary_key=True)
   nomRegion = models.CharField(max_length=100)
   adminRegion = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

   coteRegion = models.CharField(max_length=100, blank=True, null=True)

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

class ProduitsArtis(models.Model):
   idProduit = models.AutoField(primary_key=True)
   nomProduit = models.CharField(max_length=100, default="")
   prix = models.FloatField()
   origine = models.CharField(max_length=1000, blank=True)
   def __str__(self) -> str:
        return (str(self.nomProduit))
   
class Lieu(models.Model):
    idLieu = models.AutoField(primary_key=True)
    nomLieu = models.CharField(max_length=100)
    descripLieu = models.CharField(max_length=1000, blank=True)
    exigence = models.CharField(max_length=1000, blank=True)
    faitHisto = models.CharField(max_length=1000, blank=True)
    
    expressCourantes = models.CharField(max_length=1000, blank=True)
    produits_artis = models.ManyToManyField(ProduitsArtis, null=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    H_ouverture = models.TimeField(blank=True, null=True)
    H_fermeture = models.TimeField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,blank=True, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True,  blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)
    transport = models.ManyToManyField(Transport, null=True, blank=True)
    feedback=models.FloatField(default=0, blank=True)
    nmb_feedback=models.IntegerField(default=0, blank=True)
    def __str__(self) -> str:
        return self.nomLieu  
    def get_admin_id(self):
        return self.region.adminRegion.idUser
    
class Evenement(models.Model):
   idEvent = models.AutoField(primary_key=True)
   nomEvent = models.CharField(max_length=100,default="", blank=True)
   descripEvent = models.CharField(max_length=1000,default="", blank=True)
   dateEvent = models.DateField(null=True,blank=True)
   H_debut = models.TimeField(null=True,blank=True)
   H_fin = models.TimeField(null=True,blank=True)
   id_lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, null=True, blank=True)
   def __str__(self) -> str:
        return (str(self.nomEvent))
   def get_admin_id(self):
        return self.id_lieu.region.adminRegion

class Photo(models.Model):
    photoId = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='static/images', default = '')
    lieuId= models.ForeignKey(Lieu, on_delete=models.CASCADE , null=True, related_name='photos', blank=True)
    eventId = models.ForeignKey(Evenement, on_delete=models.CASCADE , null=True, related_name='images',blank=True)
    produitId = models.ForeignKey(ProduitsArtis, on_delete=models.CASCADE , null=True, related_name='pictures',blank=True)

    def __str__(self) -> str:
          return (str(self.image))

class Favoris(models.Model):
   id_favoris = models.AutoField(primary_key=True)
   idUser = models.ForeignKey(User, on_delete=models.CASCADE)
   id_lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
   def __str__(self) -> str:
        return (str(self.id_favoris))
   
class Comment(models.Model):
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    def get_lieu_name(self):
        return self.lieu.nomLieu
    def get_admin_id(self):
        return self.lieu.region.adminRegion.idUser
    @classmethod
    def get_comments_for_admin(cls, admin_id):
        return cls.objects.filter(lieu__region__adminRegion__idUser=admin_id)
class Notification(models.Model):
    adminreg = models.ForeignKey(User, on_delete=models.CASCADE)
    lieu =models.CharField(max_length=1000,default='')
    author=models.CharField(max_length=100,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.author
    
class Feedback(models.Model):
    user = models.CharField(max_length=100)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField()

class NotificationEvent(models.Model):
    idNotif = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return (str(self.idNotif))
    
class HistoryEvent(models.Model):
    idHis = models.AutoField(primary_key=True)
    Iduser = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    Idevent = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    STATUS_CHOICES = (
      ('Ajout Evenemen', 'Ajout Evenement'),
      ('Modification Evenement', 'Modification Evenement'),
      ('Suppression Evenement', 'Suppression Evenement'),
      ('Ajout lieu', 'Ajout lieu'),
      ('Modification lieu', 'Modification lieu'),
      ('Suppression lieu', 'Suppression lieu'),
        )
    Type_Action = models.CharField(max_length=100, choices=STATUS_CHOICES)

   
    def __str__(self) -> str:
        return (str(self.idHis))

class HistoryLieu(models.Model):
    idHis = models.AutoField(primary_key=True)
    Iduser = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    Idlieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    STATUS_CHOICES = (
      ('Ajout lieu', 'Ajout lieu'),
      ('Modification lieu', 'Modification lieu'),
      ('Suppression lieu', 'Suppression lieu'),
        )
    Type_Action = models.CharField(max_length=100, choices=STATUS_CHOICES)

   
    def __str__(self) -> str:
        return (str(self.idHis))

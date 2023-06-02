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
   idCategorie = models.AutoField(primary_key=True, default='')
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

   def __str__(self) -> str:
        return (self.username)

class Region(models.Model):
   numRegion = models.AutoField(primary_key=True)
   nomRegion = models.CharField(max_length=100)
   adminRegion = models.ForeignKey(User, on_delete=models.CASCADE, default='')
   def __str__(self) -> str:
        return (self.nomRegion)

class Ville(models.Model):
   idVille = models.AutoField(primary_key=True)
   nomVille = models.CharField(max_length=100)
   regionV = models.ForeignKey(Region, on_delete=models.CASCADE)
   def __str__(self) -> str:
        return (self.nomVille)
   
class MoyenTransport(models.Model):
   idTransport = models.AutoField(primary_key=True)
   typeTrans = models.CharField(max_length=100)
   def __str__(self) -> str:
        return (str(self.idTransport))

   
class Lieu(models.Model):
    idLieu = models.AutoField(primary_key=True)
    nomLieu = models.CharField(max_length=100)
    descripLieu = models.CharField(max_length=1000)
    exigence = models.CharField(max_length=1000)
    faitHisto = models.CharField(max_length=1000)
    produitArtis = models.CharField(max_length=1000, default="")
    expressCourantes = models.CharField(max_length=1000)
    longitude = models.FloatField()
    latitude = models.FloatField()
    H_ouverture = models.TimeField()
    H_fermeture = models.TimeField()
    climat = models.ForeignKey(Meteo, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    adminRegion = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    feedback=models.FloatField(default=0)
    nmb_feedbach=models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.nomLieu   
    

class Evenement(models.Model):
   idEvent = models.AutoField(primary_key=True)
   nomEvent = models.CharField(max_length=100)
   descripEvent = models.CharField(max_length=1000)
   dateEvent = models.DateField()
   H_debut = models.TimeField()
   H_fin = models.TimeField()
   lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE,default=1)
   def __str__(self) -> str:
        return (str(self.idEvent))
   def get_admin_id(self):
        return self.Lieu.adminRegion.idUser
   
#Relation de l'association entre Lieu et MoyenTransport
class Transport(models.Model):
   id_trans = models.AutoField(primary_key=True)
   id_moytrans = models.ForeignKey(MoyenTransport, on_delete=models.CASCADE)
   id_lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
   H_depart = models.TimeField()
   def __str__(self) -> str:
        return (str(self.id_trans))
   
class Comment(models.Model):
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text



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
 

    def __str__(self):
        return f"Feedback: User - {self.user}, Lieu - {self.lieu.nomLieu}"

   
   


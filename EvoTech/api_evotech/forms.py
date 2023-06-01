from django.forms import ModelForm
from django import forms
from .models import *


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields ="__all__"
        exclude = ['profile']
    

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields =['username','motdepasse']
        

class LieuForm(ModelForm):
    
    def __init__(self, *args, communes=None, **kwargs):
        super().__init__(*args, **kwargs)
        if communes is not None:
            self.fields['commune'].queryset = communes
    
    

    class Meta:
        model = Lieu
        fields = '__all__'
      

   


class EvenementForm(forms.ModelForm):
    
    def __init__(self, *args, lieux=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lieux is not None:
            self.fields['id_lieu'].queryset = lieux

    class Meta:
        model = Evenement
        fields = '__all__'




class TransportForm(forms.ModelForm):
             
    class Meta:
        model = Transport
        fields = '__all__'





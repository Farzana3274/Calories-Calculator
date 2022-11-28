from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import BMRdata


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        



class BMR_Calculater(ModelForm):
    class Meta:
        model = BMRdata
        fields = ('Gender', 'Weight', 'Height', 'Age', 'Life_style')
        widgets = {'Gender': forms.RadioSelect, 'Life_style': forms.Select(attrs={'class': 'form-control'})}
    
    def __init__(self, *args, **kwargs):
        super(BMR_Calculater, self).__init__(*args, **kwargs)
        self.fields['Weight'].widget.attrs['class'] = 'form-control'
        self.fields['Weight'].widget.attrs['placeholder'] = 'Weight in kg'
        
        self.fields['Height'].widget.attrs['class'] = 'form-control'
        self.fields['Height'].widget.attrs['placeholder'] = 'Height in cm'
        
        self.fields['Age'].widget.attrs['class'] = 'form-control'
        self.fields['Age'].widget.attrs['placeholder'] = 'Age in year'


    
        

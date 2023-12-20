from django import forms
from .models import Document
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DocumnetForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name','pdf']
        widgets = {
            'pdf': forms.FileInput(attrs={'accept': '.pdf'}),
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
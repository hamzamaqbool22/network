from django import forms
from .models import Newpost

class PostForm(forms.ModelForm):
    class Meta:
        model  = Newpost
        fields= ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'})
        }
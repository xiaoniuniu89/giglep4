from social.models import Musician
from django import forms
from .models import Post


class MusicianUpdateForm(forms.ModelForm):
    instrument = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-field'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-field'}))
    blurb = forms.CharField(max_length=100, required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':15, 'class': 'form-field-textarea'}))
    
    class Meta:
        model = Musician
        fields = ['instrument', 'location', 'blurb', 'profile_pic']


class PostForm(forms.ModelForm):
    content = forms.CharField(max_length=100, required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':15, 'class': 'form-field-textarea'}))
    class Meta:
        model = Post
        fields = ['content']
        
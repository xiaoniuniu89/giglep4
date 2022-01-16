from social.models import Musician
from django import forms
from .models import Post, Comment, Thread, Message


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
        


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=100, required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':15, 'class': 'form-field-textarea'}))
    class Meta:
        model = Comment
        fields = ['comment']



class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.Textarea(attrs={'rows':1, 'cols':1, 'class': 'form-field-textarea'}))
    
class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000, widget=forms.Textarea(attrs={'rows':4, 'cols':15, 'class': 'form-field-textarea'}))

    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'rb-txt file-upload'}))

    class Meta:
        model = Message
        fields = ['body', 'image']
    
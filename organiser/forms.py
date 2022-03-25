from django import forms
from social.models import Musician
from .models import Post, Comment, Message


class MusicianUpdateForm(forms.ModelForm):
    """
    One part of form that updates
    the user profile - second part
    comes from user update form
    """
    instrument = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-field', 'maxlength': '15'}))
    location = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={'class': 'form-field', 'maxlength': '15'}))
    blurb = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 15,
            'class': 'form-field-textarea'
        }))

    class Meta:
        """ Form fields """
        model = Musician
        fields = ['instrument', 'location', 'blurb', 'profile_pic']


class PostForm(forms.ModelForm):
    """
    Customised form for posts
    """
    content = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 15,
            'class': 'form-field-textarea'
        }))

    class Meta:
        """ Form fields """
        model = Post
        fields = ['content']


class CommentForm(forms.ModelForm):
    """
    Customised form for comments
    """
    comment = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 15,
            'class': 'form-field-textarea'
        }))

    class Meta:
        """ Form Fields """
        model = Comment
        fields = ['comment']


class MessageForm(forms.ModelForm):
    """
    Customised form for messages
    used to write DMs
    """
    body = forms.CharField(
        label='',
        max_length=1000,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 15,
            'class': 'form-field-textarea'
        }))

    class Meta:
        """ Form Fields """
        model = Message
        fields = ['body']

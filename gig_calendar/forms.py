from django import forms
from .models import Event

class DateInput(forms.DateInput):
    input_type = 'date'

class EventForm(forms.ModelForm):
    title = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-field'}))
    description = forms.CharField(max_length=100, required=True, widget=forms.Textarea(attrs={'rows':4, 'cols':15, 'class': 'form-field-textarea'}))

    class Meta:
        model = Event
        fields = ['title', 'date', 'description']
        widgets = {
            'date': DateInput(attrs={'class': 'form-field'}),
        }
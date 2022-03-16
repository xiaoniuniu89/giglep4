from django import forms
from .models import Event


class DateInput(forms.DateInput):
    """ Date input for event date field"""
    input_type = 'date'


class EventForm(forms.ModelForm):
    """
    Custom form to add class and style to the
    add event form
    """
    title = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-field'}
        )
    )
    description = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 15,
                'class': 'form-field-textarea'
            }
        )
    )

    class Meta:
        """form fields"""
        model = Event
        fields = ['title', 'date', 'description']
        widgets = {
            'date': DateInput(attrs={'class': 'form-field'}),
        }

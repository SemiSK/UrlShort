from django import forms

class FullUrlForm(forms.Form):
    full_url = forms.URLField(widget=forms.TextInput(attrs={
        'type' : 'url',
        'class' : 'form-control',
        'placeholder' : 'Place URL here',
        'required' : '',
        'autofocus' : ''
        }))

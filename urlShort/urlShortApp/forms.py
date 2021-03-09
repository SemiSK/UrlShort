from django import forms

class FullUrlForm(forms.Form):
    full_url = forms.URLField()    

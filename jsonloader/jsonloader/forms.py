from django import forms

class UploadJsonForm(forms.Form):
    file = forms.FileField()
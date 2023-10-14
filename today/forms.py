from django import forms
class FilterForm(forms.Form):
    transmission=  forms.CharField()
from django import forms

class MapsForm(forms.Form):
    start_loc = forms.CharField(label='location_field', max_length=200)
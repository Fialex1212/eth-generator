from django import forms

class PublicKeyForm(forms.Form):
    public_key = forms.CharField(label='Public Key', max_length=130, widget=forms.TextInput(attrs={'size': '64'}))

class KeyGenerationForm(forms.Form):
    generate_new = forms.BooleanField(label='Generate new keys', required=False)
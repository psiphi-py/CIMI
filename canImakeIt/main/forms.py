from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name your Kitchen'}))
    check = forms.BooleanField(required=False)
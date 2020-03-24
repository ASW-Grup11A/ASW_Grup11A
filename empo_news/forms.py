from django import forms


class SubmitForm(forms.Form):
    title = forms.CharField(max_length=10, min_length=1, label='title', label_suffix=" ")



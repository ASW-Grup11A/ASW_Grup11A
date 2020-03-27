from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SubmitForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"size": 40}), max_length=10, min_length=1, label='title',
                            label_suffix=" ")
    url = forms.CharField(widget=forms.TextInput(attrs={"size": 40}), max_length=10, min_length=1, label='url',
                          label_suffix=" ", required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 56}), label='text', label_suffix=" ",
                           required=False)

    def clean_url(self):
        text_data = self.cleaned_data['text']

        if text_data:
            raise ValidationError(_('Text field should be empty'))

        return self.cleaned_data['url']

    def clean_text(self):
        url_data = self.cleaned_data['url']

        if url_data:
            raise ValidationError(_('Url field should be empty'))

        return self.cleaned_data['text']

import re

from django import forms


class SubmitForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"size": 40}), max_length=80, min_length=1, label='title',
                            label_suffix=" ")
    url = forms.CharField(widget=forms.TextInput(attrs={"size": 40}), max_length=500, min_length=1, label='url',
                          label_suffix=" ", required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 56}), label='text', label_suffix=" ",
                           required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data['url']
        text = cleaned_data['text']

        if url and text and self.valid_url(url):
            raise forms.ValidationError('Submissions can\'t have both urls and text, so you need to pick one. '
                                        'If you keep the url, you can always post your text as a comment in the '
                                        'thread.')
        return cleaned_data

    @staticmethod
    def valid_url(url):
        return re.match("\.[a-zA-z0-9]+$", url)

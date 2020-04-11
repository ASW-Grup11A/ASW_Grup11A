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
        return "." in url


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 56}), label='', label_suffix=" ",
                              required=False)

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data['comment']

        if not comment:
            raise forms.ValidationError('Please try again.')

        return cleaned_data
        
     
class UserUpdateForm(forms.Form):
    about = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 56}), label='about', required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={"size": 40}), max_length=80, min_length=1, label='email',
                            required=True)
    showdead = forms.ChoiceField(choices=[('0', 'no'), ('1', 'yes')], label='showdead', required=True)
    noprocrast = forms.ChoiceField(choices=[('0', 'no'), ('1', 'yes')], label='noprocrast', required=True)
    maxvisit = forms.CharField(widget=forms.TextInput(attrs={"size": 10}), max_length=80, min_length=1,
                               label='maxvisit',
                               required=True)
    minaway = forms.CharField(widget=forms.TextInput(attrs={"size": 10}), max_length=80, min_length=1, label='minaway',
                              required=True)
    delay = forms.CharField(widget=forms.TextInput(attrs={"size": 10}), max_length=80, min_length=0, label='delay',
                            required=True)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class EditCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 56}), label='text', required=False)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

'''from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
          "user_name": "Your Name",
          "user_email": "Your Email",
          "text": "Your Comment"
        }

'''

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "text"]
        '''widgets = {
        'author_name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
    }'''

    def clean(self):
        author_name = self.cleaned_data['text']
        if "spam" in author_name.lower():
            raise forms.ValidationError("Le titre ne doit pas contenir le mot 'spam'.")
        return author_name

















from django import forms
from .models import Author

class AuthorSelectionForm(forms.Form):
    new_author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label='Select a new author',
        empty_label=None,
    )

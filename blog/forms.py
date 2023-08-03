from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from blog.models import Comment

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_from_email(self):
        data = self.cleaned_data["from_email"]

        if data.strip().endswith("mail.ru"):
            raise ValidationError(_("We can't send email on mail.ru emails"))

        return data

    def clean(self):
        email = self.cleaned_data["from_email"]
        subject = self.cleaned_data["subject"]

        if email.endswith("gmail.com") and "spam" in subject.lower():
            self.add_error(None, "Can't send spam emails")


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "comment_text"]

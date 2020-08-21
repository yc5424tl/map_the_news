from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

from mtn_web.models import Post, Comment, Result


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name",)


class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields["body"].widget.attrs["readonly"] = True

    class Meta:
        model = Post
        fields = ("title", "public", "body")
        disabled = "body"


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"cols": 75, "rows": 12, "class": "resizable", "required": True}
        ),
        label="",
    )


class NewQueryForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ("argument", "query_type")


class SaveResultForm(forms.ModelForm):
    # TODO add option to publish in this form
    class Meta:
        model = Result
        fields = ("public",)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body")


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "height": "60em",
                    "width": "80vw",
                    "overflow-y": "scroll",
                    "padding": "1em",
                }
            ),
        }


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hi'}
    ))


class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email"]


class LogoutForm(forms.ModelForm):
    class Meta:
        model = None
        fields = None


class NewUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
        ]


class UpdateUserForm(UserChangeForm):
    model = get_user_model()
    fields = ["email"]

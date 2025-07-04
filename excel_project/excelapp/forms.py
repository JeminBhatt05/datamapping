from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class UploadFileForm(forms.Form):
    file = forms.FileField()

class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email")
    mobile = forms.CharField(max_length=15, label="Mobile Number")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Mobile Number")
    password = forms.CharField(widget=forms.PasswordInput)
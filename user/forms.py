from django import forms
from . import models

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("password wrong"))
            return email
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

class SignUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("email", "nickname",)

    nickname = forms.CharField(max_length=20, min_length=2)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.User.objects.get(email=email)
            self.add_error("email", forms.ValidationError("User already exists"))
        except models.User.DoesNotExist:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        try:
            models.User.objects.get(nickname=nickname)
            self.add_error("nickname", forms.ValidationError("닉네임이 이미 존재합니다."))
        except models.User.DoesNotExist:
            return nickname

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        
        if password != password2:
            raise forms.ValidationError("password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        nickname = self.cleaned_data.get("nickname")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
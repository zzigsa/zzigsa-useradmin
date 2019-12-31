import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile # FileField 쓸 때 필요한거 아직은 안쓰임
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins

# Create your views here.

class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "user/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    
    template_name = "user/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass

    return redirect(reverse('core:home'))

def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/user/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )
class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/user/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kaccount_email", None)
        # if email is None:
        #     print("email is none")
        #     raise KakaoException()
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        try:
            if email is None:
                user = models.User.objects.get(username=nickname)
            else:
                user = models.User.objects.get(email=email)
                if user.login_method != models.User.LOGIN_KAKAO:
                    raise KakaoException()
        except models.User.DoesNotExist:
            if email is None:
                user = models.User.objects.create(
                    username=nickname,
                    nickname=nickname,
                    login_method=models.User.LOGIN_KAKAO,
                    email_verified=True,
                )
            else:
                user = models.User.objects.create(
                email=email,
                username=email,
                nickname=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
                )
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("user:login"))


class UserProfileView(DetailView):

    model = models.User
    # context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello!"
        return context


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    
    model = models.User
    template_name = "user/update-profile.html"
    fields = ("nickname",)

    def get_object(self, queryset=None):
        return self.request.user

    # 플레이스홀더 만드는 법
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #     form.fields['nickname'].widget.attrs = {"placeholder": "닉네임"}
    #     return form

    success_message = "Profile Updated"

class UpdatePassword(
    mixins.EmailLoginOnlyView,
    mixins.LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView
):
    
    template_name = "user/update-password.html"
    success_message = "Password updated"
    
    def get_success_url(self):
        return self.request.user.get_absolute_url()
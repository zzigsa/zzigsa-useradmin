import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string

# Create your models here.
class User(AbstractUser):

    """ Custom User Model """

    ZZIGSA_NOT_YET = "not yet"
    ZZIGSA_APPROVED = "approved"
    ZZIGSA_DENIED = "denied"

    ZZIGSA_CHOICES = (
        (ZZIGSA_NOT_YET, "Not yet"),
        (ZZIGSA_APPROVED, "Approved"),
        (ZZIGSA_DENIED, "Denied"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_KAKAO, "Kakao"),
    )

    nickname = models.CharField(max_length=20, unique=True)
    zzigsa = models.CharField(choices=ZZIGSA_CHOICES,  max_length=10, default=ZZIGSA_DENIED)

    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    def get_absolute_url(self):
        return reverse("user:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", {'secret': self.email_secret})
            send_mail(
                "Verify Zzigsa Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=True,
                html_message=html_message,
            )
            self.save()
        return

    def __str__(self):
        return self.nickname
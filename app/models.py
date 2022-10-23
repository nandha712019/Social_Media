# Create your models here.
from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date


# ---- user model started----
def validate_birth_date(value):
    if value > (date.today() - timedelta(days=6 * 365)):
        raise ValidationError(
            'Child age below 6 is not allowed to create account'
        )


class Users(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    date_of_birth = models.DateField('Your Date of birth', blank=False, validators=[validate_birth_date],
                                     default=datetime.today())
    email = models.EmailField(unique=True, blank=False, null=False)
    country = CountryField(blank=False)
    user_profile_picture = models.ImageField(upload_to="Profile_Images_Folder/", default="", null=False, blank=False)
    description = models.TextField(max_length=200, default="")
    work = models.CharField(max_length=20, default="")
    login_details = models.CharField("active session details", max_length=25, blank=False, null=False,
                                     choices=[
                                         ("is_login", True),
                                         ("last_login", datetime.now())
                                     ], default="last_login")


def __str__(self):
    return self.get_username()

# ----user model ended----

# ---- media model started ----


class Media(models.Model):
    Media_id = models.TextField(primary_key=True)
    Media_link = models.FilePathField(verbose_name="Media_link")

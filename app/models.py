# Create your models here.
import os
from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, date
#from uuid import uuid5


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
                                     default=timezone.now())
    email = models.EmailField(unique=True, blank=False, null=False)
    country = CountryField(blank=False)
    description = models.TextField(max_length=200, default="", blank=True, null=True)
    work = models.CharField(max_length=20, default="")
    login_details = models.CharField("active session details", max_length=25, blank=False, null=False,
                                     choices=[
                                         ("is_login", True),
                                         ("last_login", datetime.now())
                                     ], default="last_login")


def __str__(self):
    return self.get_username()

# ----user model ended----


# ----media model started ----


def profile_picture_location_setter(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return 'Profile_Images_Folder/{userid}/{userid}{randomstring}{ext}'.format(userid=instance.user, randomstring=datetime.now(), ext=file_extension)


class Media(models.Model):
    media_id = models.IntegerField(primary_key=True, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_profile_picture = models.ImageField(upload_to=profile_picture_location_setter, null=False, blank=False)
    media_link = models.FileField(verbose_name="Media_link", unique=True, upload_to="Media_Files")
    media_Title = models.CharField(max_length=20, blank=True)
    media_description = models.TextField(max_length=200, blank=True)
    media_hashtag = models.TextField(max_length=200, blank=True, null=True)
    media_uploaded_time = models.DateTimeField(default=timezone.now(), blank=False, null=False, editable=False)
    media_type = models.CharField(max_length=20, choices=[
        ("image", "image"),
        ("video", "video")
    ])
    thumbnail = models.ImageField(upload_to="Media_Thumbnails")
    media_location = models.CharField(max_length=20, blank=True)
    media_viewer = models.CharField(max_length=20, choices=[
        ("Friends", "Friends"),
        ("Public", "Public")
    ])

    def save(self, *args, **kwargs):
        filename = self.media_link
        file = os.path.splitext(str(filename))
        image_formats = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif",
                         ".psd",
                         ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2"]
        video_formats = []
        file_type=""
        if file[1] in image_formats:
            self.media_type = "images"
        elif file[1] in video_formats:
            self.media_type = "videos"
        super(Media, self).save(*args, **kwargs)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     file = os.path.splitext(self.media_link)


class MediaFavourites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    media_id = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "media_id"]


class MediaViews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    media_id = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "media_id"]

# ----*media models ended*----

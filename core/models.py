from django.db import models

# Create your models here.


class UploadImage(models.Model):
    img = models.ImageField('images')


class Log(models.Model):
    masked_user = models.IntegerField('masked_user')
    un_masked_user = models.IntegerField('un_masked_user')
    created_at = models.DateTimeField(auto_now_add=True)

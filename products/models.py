from django.db import models
from django_resized import ResizedImageField


imagesDire = 'images/'
codesSourceDire = 'codeFiles/'
appsSourceDire = 'appFiles/'


# class Category(models.model):
#     name = models.CharField(max_length=50, blank=True, null=False)
#     description = models.TextField(blank=True, null=False)

#     def __str__(self):
#         return self.name


class ProgrammeCode(models.Model):
    name = models.CharField(max_length=50, blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    dateAdded = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(null=True)
    cover = ResizedImageField(
        size=[500, None], blank=True, null=True, upload_to=imagesDire)
    demo = models.URLField(blank=True, null=True)
    sourceFile = models.FileField(
        blank=False, null=True, upload_to=codesSourceDire)

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=False, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(null=True)
    cover = ResizedImageField(
        size=[500, None], blank=True, null=True, upload_to=imagesDire)
    demo = models.URLField(blank=True, null=True)
    sourceFile = models.FileField(
        blank=False, null=True, upload_to=appsSourceDire)

    def __str__(self):
        return self.name

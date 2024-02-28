from django.db import models
from members.models import Member
from django_resized import ResizedImageField

imagesDire = 'images/'
codesSourceDire = 'codeFiles/'
appsSourceDire = 'appFiles/'
# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(blank=False, max_length=50)
    category = models.ForeignKey(
        "ProductCategory", verbose_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    pic = ResizedImageField(
        size=[500, None], blank=True, null=True, upload_to=imagesDire)
    video = models.URLField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory, verbose_name="Category",
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comments(models.Model):
    member = models.ForeignKey(
        Member, verbose_name='user', related_name='prod_commentator', on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    product = models.ForeignKey(
        Product, related_name='product', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    isActive = models.BooleanField(default=False)

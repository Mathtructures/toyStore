from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from hashlib import sha256
from django.utils.translation import gettext as _
from products.models import ProgrammeCode, Application


class ShoppingCart(models.Model):
    totalPrice = models.IntegerField(default=0)
    appsSection = models.ManyToManyField(Application, blank=True)
    codeProgsSection = models.ManyToManyField(ProgrammeCode, blank=True)

    def calTotalPrice(self):
        price = 0
        for app in self.appsSection.all():
            price += app.price
        for code in self.codeProgsSection.all():
            price += code.price
        self.totalPrice = price
        return price

    def clearCart(self):
        self.totalPrice = 0
        self.appsSection.clear()
        self.codeProgsSection.clear()


class MemberManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, email,
                    is_superuser=False, is_admin=False, is_staff=False,
                    is_active=True, **extra_fields):
        user = self.model(username=username, email=self.normalize_email(email))
        first_name = extra_fields.get('first_name')
        last_name = extra_fields.get('last_name')
        cellphone = extra_fields.get('cellphone')
        quote = extra_fields.get('quote')
        user.first_name = first_name
        user.last_name = last_name
        user.cellphone = cellphone
        user.quote = quote
        user.cartItems = ShoppingCart.objects.create()
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password,
                         is_superuser=True, is_admin=True, is_staff=True,
                         is_active=True, **extra_fields):
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        first_name = extra_fields.get('first_name')
        last_name = extra_fields.get('last_name')
        cellphone = extra_fields.get('cellphone')
        quote = extra_fields.get('quote')
        user.first_name = first_name
        user.last_name = last_name
        user.cellphone = cellphone
        user.quote = quote
        user.cartItems = ShoppingCart.objects.create()
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user


# Create your models here.
class Member(AbstractBaseUser):
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    username = models.CharField(max_length=120, null=True, unique=True)
    email = models.CharField(max_length=120, null=True, unique=True)
    cellphone = models.BigIntegerField(null=True, blank=True)
    quote = models.CharField(max_length=120, null=True, blank=True)
    registrationDate = models.DateField(null=True, blank=True)

    listOfAllPurchases = models.TextField(blank=True, null=True)
    cartItems = models.OneToOneField(
        'ShoppingCart', on_delete=models.CASCADE, null=True, blank=True)
    purchasedApps = models.ManyToManyField(
        Application, blank=True, related_name="accessedApps")
    purchasedProgCodes = models.ManyToManyField(ProgrammeCode, blank=True,
                                                related_name="accessedProgCodes")

    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def delete(self):
        self.cartItems.delete()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes,always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes,always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def send_confirmation_mail(self):
        mail_subject = _('Numera account activation')
        recipient = self.email
        userHS = sha256(self.username.encode('utf_8')).hexdigest()
        html_message = render_to_string('members/confirmationMail.html', {'id': self.id,
                                                                          'userHS': userHS,
                                                                          'fname': self.first_name})
        message = strip_tags(html_message)
        text_content = f"{_('Hello')} {self.first_name}." +\
            f"{_('Please click the verification link below to verify your email.')}" +\
            f"{_('If you have not registered to http://www.numera.ir please ignore this message.')}"
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            subject = mail_subject
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [recipient,]
            message = message
            # EmailMessage(subject,message,email_from,
            #              recipient_list,connection=connection).send()
            msg = EmailMultiAlternatives(
                subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        return 0

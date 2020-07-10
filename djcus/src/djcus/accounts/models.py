from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from .utils import code_generator
# Create your models here.


class MyUserManager(BaseUserManager):           # This is a database field save username and password
    def create_user(self, username=None, email=None, password=None): 
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        	username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)     # save the password
        return user

    def create_superuser(self, email, username=None, password=None): #resposible for admin and staff create
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
        	username,
            email,
            password=password
            # username =username,
        )
        user.is_admin = True          #mention admin
        user.is_staff = True          #mention staff
        user.save(using=self._db)     # save the created create_superuser
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$' # for valiadtion
#As our regular expression tells to contain all. but we also have email field. which
#means that our username also contain @ symbol and email as well which create the
#repitation or duplication. to prevent from that we have to skip username with @
#symbol for that USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$', we can update this be
#deleting @ symbol.

class MyUser(AbstractBaseUser):      # This is a db create(table) data can access by  using MyUser.objects.all()
    username = models.CharField(max_length=255, validators=[
                                                 RegexValidator(
                                                 	   regex = USERNAME_REGEX,
                                                      message = 'username must be AlphaNumeric',
                                                      code = 'Invalid username'
                                                   )] ,# Python regular expression validator field
                                                 unique = True,
                                              )      

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)  #For login
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'    # username field used for login purpose
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    key = models.CharField(max_length=250)
    exp = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
       self.key = code_generator()
       super(ActivationProfile,self).save(*args,**kwargs)

def post_save_activation_receiver(sender,instance,created,*args,**kwargs):
    if created:
        print("send email")
        print("activation create")
        # url = "http/joinrushi.com/activate/" + instance.key
        # send_email()
post_save.connect(post_save_activation_receiver,sender=ActivationProfile)

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	city = models.CharField(max_length=255, null=True, blank=True)
	content = models.TextField(max_length=250, null=True, blank=True)
	integer = models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)

# def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		try:
#             Profile.objects.create(user=instance)
#         except:
#             pass
# post_save.connect(post_save_user_model_receiver,sender=settings.AUTH_USER_MODEL)  
  
def post_save_user_model_receiver(sender,instance,created,*args,**kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass
post_save.connect(post_save_user_model_receiver,sender=settings.AUTH_USER_MODEL)
#This signals get trigger after creating a user
# The profile won't show to admin dashboard because of singles and singles only trigger when user created

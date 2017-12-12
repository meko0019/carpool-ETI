from django.db import models
from django.core.mail import send_mail
# from django.contrib.auth.models import PermissionMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator
import datetime

class MyUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		'''
		creates and saves a User with the give email and password
		'''
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(email = self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		'''
		creates and saves a superuser with the given email and password
		'''
		user = self.create_user(email, password=password)
		user.is_admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	first_name = models.CharField(max_length=30, null = True)
	last_name = models.CharField( max_length=30, null = True)
	street = models.CharField(max_length = 255, default='')
	city = models.CharField(max_length = 100, default = '')
	zipcode = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(99999)])
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def get_full_name(self):
		'''
		returns the first and last name of the user
		'''
		full_name = '%s %s' %(self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
		returns the first name of the user
		'''
		return self.first_name

	def __str__(self):

		return ('%s  %s' %(self.first_name, self.email)) 

	def has_perm(self, perm, obj=None):
		'''
		Returns True if the user has the specified permission, 
		where perm is in the format "<app label>.<permission codename>".
		'''
		return True

	def has_module_perms(self, app_label):
		'''
		Returns True if the user has any permissions in the given package
		(the Django app label). If the user is inactive, this method will 
		 always return False
		'''
		return True

	@property
	def is_staff(self):

		return self.is_admin


class Trip(models.Model):
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, unique=True)
	date = models.DateTimeField()
	street = models.CharField(max_length = 255)
	city = models.CharField(max_length = 100)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField(blank=True, validators=[MaxValueValidator(99999)])
	created_at = models.DateTimeField(auto_now_add=True)	
	full_address = models.CharField(max_length = 255)
	#TODO: add more fields such as last_update, and other user related fields to make Trips more flexible

	def __str__(self):          
		return ('%s,  %s %s %d' %(self.street, self.city, self.state, self.zipcode)) 

# trip3 = Trip.objects.create(created_by=user, name='xcel', date = '2017-12-14 2:20', street = '199 W Kellogg Blvd', city='St Paul', state='MN', zipcode = 55102)

class Waypoint(models.Model):
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	trip = models.ForeignKey(Trip, null=True, on_delete=models.CASCADE)
	street = models.CharField(max_length = 255)
	city = models.CharField(max_length = 100)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField(blank=True, validators=[MaxValueValidator(99999)])
	full_address = models.CharField(max_length = 255)

	def __str__(self):          
		return ('%s,  %s %s %d' %(self.street, self.city, self.state, self.zipcode))


class Carpool(models.Model):
	waypoint = models.ManyToManyField(Waypoint, related_name = 'carpool_waypoint')
	start = models.ManyToManyField(Waypoint, related_name = 'carpool_start')
	trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

	def __str__(self):          
		return ('carpool  %d' %(self.pk))


# 1178 Burnsville Center, Burnsville, MN 55306


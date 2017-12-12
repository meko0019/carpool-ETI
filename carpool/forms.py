from django import forms
from .models import User, Trip, Waypoint
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
	'''
	A form for creating new users, includes all the required fields plus a repeated password
	'''
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
	password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

	class Meta:
   		model = User
   		fields = ('first_name','last_name', 'email', 'password1', 'password2', )
   		widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),

        }


   		labels = {}
   		for field in fields:
   			labels.update({field: ''})



	def clean_password2(self):
  		#check that the passwords match
  		password1 = self.cleaned_data.get("password1")
  		password2 = self.cleaned_data.get("password2")

  		if password1 and password2 and (password1 != password2):
  			raise forms.ValidationError("Passwords don't match")
  		return password2

	def save(self, commit=True):
  		#save the password in hashed format
  		user = super(UserCreationForm, self).save(commit=False)
  		user.set_password(self.cleaned_data["password1"])
  		if commit:
  			user.save()
  		return user

class UserChangeForm(forms.ModelForm):
	'''
	A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
	'''
	password = ReadOnlyPasswordHashField()

	class  Meta:
		model = User
		fields = ('email', 'password','is_active','is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]



class PostForm(forms.ModelForm):
	'''
	A form for creating new Trip posts 
	'''
	class Meta:
   		model = Trip
   		# date = forms.DateTimeField(input_formats = ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
					# 									 '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
					# 									 '%Y-%m-%d',             # '2006-10-25'
					# 									 '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
					# 									 '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
					# 									 '%m/%d/%Y',             # '10/25/2006'
					# 									 '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
					# 									 '%m/%d/%y %H:%M',       # '10/25/06 14:30'
					# 									 '%m/%d/%y']             # '10/25/06'
					# 								)
   		fields = ('name','date', 'street', 'city', 'state', 'zipcode')
   		widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Enter a name for your trip'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control rounded', 'placeholder': 'Time and date: YYYY-MM-DD H:M'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'zipcode'}),

        }


   		labels = {}
   		for field in fields:
   			labels.update({field: ''})

class SelectForm(forms.ModelForm):
	'''
	A form for creating waypoint info
	'''
	class Meta:
   		model = Waypoint
   		fields = ('trip', 'street', 'city', 'state', 'zipcode')
   		widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'zipcode'}),
            'trip': forms.Select(attrs={'class': 'form-control'}),

        }


   		labels = {}
   		for field in fields:
   			labels.update({field: ''})

   		#TODO: give user option to save addresses as home, work, etc and select from options 



class CarpoolForm(forms.Form):
	'''
	A form for extracting waypoint data for route computation
	'''

	start = forms.ModelChoiceField(widget = forms.Select(attrs={'class': 'form-control', 'id':'start'}), queryset=None)
	waypoints = forms.ModelMultipleChoiceField(widget = forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'waypoints'}), queryset=None)
	end = forms.ModelChoiceField(widget = forms.Select(attrs={'class': 'form-control', 'id': 'end'}), queryset=None)
	
	def __init__(self, trips, waypoints, *args, **kwargs):
		super(CarpoolForm, self).__init__(*args, **kwargs)
		self.fields['start'].queryset= waypoints
		self.fields['start'].to_field_name= 'full_address'
		self.fields['waypoints'].queryset = waypoints
		self.fields['waypoints'].to_field_name= 'full_address'
		self.fields['end'].queryset = trips
		self.fields['end'].to_field_name= 'full_address'





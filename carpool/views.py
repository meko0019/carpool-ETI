# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import Trip, Waypoint, User
from .forms import UserCreationForm, PostForm, SelectForm, CarpoolForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms

# Create your views here.
def home(request):

	if request.user.is_authenticated():
		users = User.objects.all()
		args = {'user': request.user, 'users': users}
		return render(request, 'index.html', args)
	else:
		return redirect('signup')



def signup(request):
	if request.user.is_authenticated():
		return redirect('/home')

	else:
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
				user = form.save()
				if user is not None:
					login(request, user)
					return redirect('home')

			else:
					#TODO: check error code and propose a fix
					return redirect('invalid')

		else:
			form = UserCreationForm()
			return render(request, 'signup.html', {'form': form})
			
@login_required
def post(request):
	''' 
	We will use the email field to get the user since each email is unique
	TODO: provide alterative formats for dates, then span with a calendar JS widget
	'''

	user = User.objects.get(email=request.user.email)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.created_by = user
			form.save()
			return redirect('home')
		else:

			#TODO: do some error handling here 
			return redirect('invalid')
			
	else:
		form = PostForm()
		args = {'user': user, 'form': form}

		return render(request, 'post.html', args)

@login_required
def select(request):
	''' 
	TODO: give user option to save most common addresses like home and work, and give them select option 

	'''

	#We will use the email field here also to get the user 
	user = User.objects.get(email=request.user.email)
	trips = Trip.objects.all()

	if request.method == 'POST':
	    form = SelectForm(request.POST)
	    if form.is_valid():
	        form = form.save(commit=False)
	        form.created_by = user
	        form.full_address = " ".join([form.POST['street'], form.POST['city'], form.POST['state'], form.POST['zipcode']])
	        form.save()
	        return redirect('home')
	    else:
	    	#TODO: check form validation errors and propose a fix 
	    	return redirect('invalid')

	else:
	    form = SelectForm(initial = {'trip': trips.get(pk=1)})
	    args = {'user': user, 'form': form, 'trips': trips}
	    
	    return render(request, 'select.html', args)

@login_required
def carpool(request):
	''' 
	We will use the email field here also to get the user since each email is unique
	TODO: 
	'''

	waypoints = Waypoint.objects.all()
	trips = Trip.objects.all()

	if request.method == 'POST':
	    form = CarpoolForm(trips, waypoints, request.POST)
	    # if form.is_valid():
	    #     form.save()
	    #     return redirect('home')
	    # else:
	    # 	#TODO: check form validation errors and propose a fix 
	    # 	return redirect('invalid')

	else:
	    form = CarpoolForm(waypoints=waypoints, trips = trips)
	    args = {'user': request.user, 'form': form, 'trips': trips, 'waypoints': waypoints}
	    
	    return render(request, 'carpool.html', args)



def invalid(request):
	return render(request, 'invalidform.html')



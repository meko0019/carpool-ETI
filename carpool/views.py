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
	user = request.user
	if user.is_authenticated():
		'''
		create some initial trips and waypoints for demo purposes 

		'''
		if Trip.objects.count() == 0:
			trip1 = Trip(created_by=user, name='xcel', date = '2017-12-14 12:20', street = '199 W Kellogg Blvd', 
				city='St Paul', state='MN', zipcode = 55102, full_address='199 W Kellogg Blvd, St Paul MN 55102')
			trip2 = Trip(created_by=user, name='work', date = '2017-12-15 8:20', street = '200 SE Oak St', 
				city='Minneapolis', state='MN', zipcode = 55455, full_address='200 SE Oak St Minneapolis, MN 55455')
			trip1.save()
			trip2.save()


		if Waypoint.objects.count() == 0:
			wp1 = Waypoint(created_by=user, street = '60 E Broadway', city='Bloomington', state='MN', zipcode = 55425, full_address='60 E Broadway Bloomington, MN 55425')
			wp2 = Waypoint(created_by=user, street = '1178 Burnsville Center', city='Burnsville', state='MN', zipcode = 55306, full_address='1178 Burnsville Center Burnsville, MN')
			wp1.save()
			wp2.save()

		args = {'user': user}
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
	TODO: provide alterative formats for dates, then span with a JS calendar widget
	'''

	user = User.objects.get(email=request.user.email)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.created_by = user
			form.full_address = " ".join([form.POST['street'], form.POST['city'], form.POST['state'], form.POST['zipcode']])
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
	    form = SelectForm()
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



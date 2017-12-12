carpool-ETI
====================================

## Description

A simple carpool app built using Google Maps API. The app uses 3 models: Trip, Waypoint, and Carpool which represent 
destination, waypoint locations to be included in route, and the final route, respectively. 

## Features 
- Post a trip (destination)
- Select from existing trips 
- Compute route 

## Installation (using Python 3.x)

$ git clone https://github.com/meko0019/carpool-ETI.git

$ virtualenv venv && source venv/bin/activate 

$ cd carpool-ETI/carpool_ETI

$ pip install -r requirements.txt

## Usage

- cd into the BASE dir

$ python manage.py makemigrations 

$ python manage.py migrate

$ python createsuperuser

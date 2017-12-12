from django.conf.urls import url, include 
from . import views
from django.contrib.auth.views import (login, logout, password_reset, password_reset_done,
 password_reset_confirm, password_reset_complete )


#TODO: finish user management (pswrd reset, profile edit, etc )

urlpatterns = [
	url(r'^$', views.home, name = 'home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout,{'next_page': 'home'}, name='logout'),
    url(r'^post/$', views.post, name='post'),
    url(r'^select/$', views.select, name='select'),
    url(r'^carpool/$', views.carpool, name='carpool'),
    url(r'^invalid/$', views.invalid, name='invalid'),


]
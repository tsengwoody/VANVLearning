from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^material/create/$', views.material_create, name='material_create'),
	url(r'^material/creategroup/$', views.material_creategroup, name='material_creategroup'),
]
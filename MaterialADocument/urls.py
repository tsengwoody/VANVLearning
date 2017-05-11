from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^material/create/$', views.material_create, name='material_create'),
	url(r'^material/creategroup/$', views.material_creategroup, name='material_creategroup'),
	url(r'^get_form_info/(?P<type>\w+)$', views.get_form_info, name='get_form_info'),
]
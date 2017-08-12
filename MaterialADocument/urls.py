from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^material_create/$', views.material_create, name='material_create'),
	url(r'^material_update/(?P<type>\w+)/(?P<id>\d+)/$', views.material_update, name='material_update'),
	url(r'^material_creategroup/$', views.material_creategroup, name='material_creategroup'),
	url(r'^materialgroup_update_order/(?P<id>\d+)/$', views.materialgroup_update_order, name='materialgroup_update_order'),
	url(r'^material_view/(?P<type>\w+)/(?P<id>\d+)$', views.material_view, name='material_view'),
	url(r'^material_list/(?P<type>\w+)$', views.material_list, name='material_list'),
	url(r'^material_delete/$', views.material_delete, name='material_delete'),
	url(r'^get_form_info/(?P<type>\w+)$', views.get_form_info, name='get_form_info'),
	url(r'^document_create/$', views.document_create, name='document_create'),
	url(r'^document_update/(?P<id>\d+)/$', views.document_update, name='document_update'),
	url(r'^document_update_order/(?P<id>\d+)/$', views.document_update_order, name='document_update_order'),
]
# coding=utf-8
from django.shortcuts import render

# Create your views here.

def home(request, template_name='users/home.html'):
	return render(request, template_name, locals())

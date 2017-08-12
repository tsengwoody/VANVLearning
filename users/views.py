# coding=utf-8
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render

import json

# Create your views here.

def login(request, template_name='users/login.html', *args, **kwargs):
	response = {}
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if not form.is_valid():
			response['status'] = 'error'
			response['message'] = u'表單驗證失敗，' + str(form.errors)
			return HttpResponse(json.dumps(response), content_type="application/json")
		response['status'] = 'success'
		response['message'] = u'登錄成功'
		return HttpResponseRedirect(
			'/',
			content=json.dumps(response),
			content_type="application/json"
		)
	if request.method == 'GET':
		return render(request, template_name, locals())

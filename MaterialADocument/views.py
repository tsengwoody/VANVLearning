# coding=utf-8
from django.shortcuts import render

# Create your views here.

from .forms import *
from .models import *

def material_create(request, template_name='MaterialADocument/material_create.html'):
	selectForm = SelectForm()
	textForm = TextForm()
	tfForm = TrueFalseForm()
	choiceForm = ChoiceForm()
	optionForm = OptionForm()
	descriptionForm = DescriptionForm()
	return render(request, template_name, locals())

def material_creategroup(request, template_name='MaterialADocument/material_creategroup.html'):
	return render(request, template_name, locals())

def get_form_info(request, template_name='MaterialADocument/get_form_info.html', *args, **kwargs):
	if kwargs['type'] in ['TextForm', 'TrueFalseForm', 'ChoiceForm', 'DescriptionForm', ]:
		exec("form = {}()".format(kwargs['type']))
	else:
		from django.http import HttpResponseServerError
		return HttpResponseServerError(u'Server Error: 指定的Form類型不存在')
	from collections import defaultdict
	field_info = defaultdict(dict)
	for id, field in enumerate(form):
		field_info[id]['name'] = field.name
		field_info[id]['value'] = field.value()
		field_info[id]['type'] = field.field.widget.__class__.__name__
		field_info[id]['attrs'] = field.field.widget.attrs
		field_info[id]['label'] = field.field.label
		field_info[id]['help_text'] = field.field.help_text
		try:
			field_info[id]['choices'] = field.field.widget.choices
		except:
			pass
	field_info['SubjectToTopic'] = {}
	for subject in Subject.objects.all():
		field_info['SubjectToTopic'][subject.name] = [topic.name for topic in subject.topic_set.all()]
	response = field_info
	import json
	s = json.dumps(response)
	if request.is_ajax():
		from django.http import HttpResponse
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return render(request, template_name, locals())

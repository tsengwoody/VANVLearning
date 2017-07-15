# coding=utf-8
from django.core.urlresolvers import reverse
from django.db.models import F,Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from collections import defaultdict
import json
import re
# Create your views here.

from .forms import *
from .models import *

def material_create(request, template_name='MaterialADocument/material_create.html'):
	user = User.objects.get(username='root')
	response = defaultdict(dict)
	if request.method == 'POST':
		materialForm = MaterialForm()
		try:
			m = materialForm.fill(request.POST, True, user)
		except TypeError as e:
			return HttpResponseServerError(u'Server Error: 指定的類型不存在')
		except ValueError as e:
			response['status'] = 'error'
			response['message'] = u'製作素材失敗：{}'.format(str(e))
			return HttpResponse(json.dumps(response), content_type="application/json")

		#製作素材成功並顯示結果
		response['status'] = 'success'
		response['message'] = u'製作素材成功！'
		return HttpResponseRedirect(
			reverse(
				'MaterialADocument:material_view',
				kwargs={
					'type': m[0].__class__.__name__,
					'id': m[0].id,
				},
			),
			content=json.dumps(response),
			content_type="application/json"
		)
	if request.method == 'GET':
		return render(request, template_name, locals())

def material_creategroup(request, template_name='MaterialADocument/material_creategroup.html'):
	p=re.compile(r'material-(?P<item>\d+)-(?P<key>.+)')
	user = User.objects.get(username='root')
	main = {}
	data = defaultdict(dict)
	response = defaultdict(dict)
	if request.method == 'POST':

		#將POST資料分項存入對應項次的dict
		for k,v in request.POST.iteritems():
			search = p.search(k)
			if search:
				data[search.group('item')].update({search.group('key'): v})
			else:
				main.update({k: v})

		#群組素材建立
		materialForm = MaterialForm()
		try:
			main_material = materialForm.fill(main, True, user)
		except TypeError as e:
			return HttpResponseServerError(u'Server Error: 指定的類型不存在')
		except ValueError as e:
			response['status'] = 'error'
			response['message'] = u'製作素材{0}失敗：{1}'.format('main', str(e))
			return HttpResponse(json.dumps(response), content_type="application/json")

		#群組素材的子素材建立
#製作素材失敗需將相關已建立的素材刪除做法
#1. 將群組母素材刪除
#2.群組母素材刪除時，會尋找有關聯的GroupMaterialDetail刪除(models.py)
#3. GroupMaterialDetail刪除時，會尋找有關聯的Material刪除(models.py)

		for k,v in data.iteritems():
			materialForm = MaterialForm()
			try:
				m = materialForm.fill(v, True, user)
			except TypeError as e:
				main_material[0].delete()
				return HttpResponseServerError(u'Server Error: 指定的類型不存在')
			except ValueError as e:
				main_material[0].delete()
				response['status'] = 'error'
				response['message'] = u'製作素材{0}失敗：{1}'.format(k, str(e))
				return HttpResponse(json.dumps(response), content_type="application/json")

			try:
				mgd = MaterialGroupDetail.objects.create(material_group=main_material[0], material=m[0], seq=int(k))
			except ValidationError as e:
				main_material[0].delete()
				response['status'] = 'error'
				response['message'] = u'製作素材{0}失敗：{1}'.format(k, str(e))
				return HttpResponse(json.dumps(response), content_type="application/json")

		#製作素材成功並顯示結果
		response['status'] = 'success'
		response['message'] = u'製作素材成功！'
		return HttpResponseRedirect(
			reverse(
				'MaterialADocument:material_view',
				kwargs={
					'type': main_material[0].__class__.__name__,
					'id': main_material[0].id,
				},
			),
			content=json.dumps(response),
			content_type="application/json"
		)
	if request.method == 'GET':
		return render(request, template_name, locals())

def material_view(request, template_name='MaterialADocument/material_view.html', *args, **kwargs):
	if kwargs['type'] not in ['Text', 'TrueFalse', 'Choice', 'Description', 'MaterialGroup', ]:
		return HttpResponseServerError(u'Server Error: 指定的Material類型不存在')
	if request.method == 'GET' and request.is_ajax():
		exec(
			'material = {0}.objects.get(id={1})'.format(kwargs['type'], kwargs['id'])
		)
		content = material.serialized()
		content.update({'type': kwargs['type']})
#		if isinstance(material, MaterialGroup):
#			print(content)

		response = {
			'status': 'success',
			'message': u'獲取素材{0}-{1}成功！'.format(kwargs['type'], kwargs['id']),
			'content': content,
		}
		return HttpResponse(content = json.dumps(response), content_type="application/json")
	elif request.method == 'GET' and not request.is_ajax():
		return render(request, template_name, locals())

def material_list(request, template_name='MaterialADocument/material_list.html', *args, **kwargs):
	if kwargs['type'] not in ['Text', 'TrueFalse', 'Choice', 'Description', 'MaterialGroup', ]:
		return HttpResponseServerError(u'Server Error: 指定的Material類型不存在')
	if request.method == 'GET' and request.is_ajax():
		exec(
			'''materials = {0}.objects.filter(
				Q(privacy=Material.PRIVACY['PUBLIC'])
				| Q(create_user=None)
			)'''.format(kwargs['type'])
		)
		content = {}
		for index,material in enumerate(materials):
			content[index] = material.serialized_abstract()
		response = {
			'status': 'success',
			'message': u'獲取素材{0}列表成功！'.format(kwargs['type']),
			'content': content,
		}
		return HttpResponse(content = json.dumps(response), content_type="application/json")
	elif request.method == 'GET' and not request.is_ajax():
		return render(request, template_name, locals())

def get_form_info(request, template_name='MaterialADocument/get_form_info.html', *args, **kwargs):
	if kwargs['type'] in ['TextForm', 'TrueFalseForm', 'ChoiceForm', 'DescriptionForm', OptionForm, ]:
		exec("form = {}()".format(kwargs['type']))
	else:
		return HttpResponseServerError(u'Server Error: 指定的Form類型不存在')
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
		field_info['SubjectToTopic'][subject.id] = [[topic.id, topic.name] for topic in subject.topic_set.all()]
	response = field_info
	if request.is_ajax():
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return render(request, template_name, locals())

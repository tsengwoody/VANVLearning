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

def material_create(request, template_name='MaterialADocument/material_create.html', *args, **kwargs):
	if request.method == 'POST':
		materialForm = MaterialForm()
		try:
			m = materialForm.create(request.POST, True, request.user)
		except TypeError as e:
			return HttpResponseServerError(u'Server Error: 指定的類型不存在')
		except ValueError as e:
			response = {
				'status': 'error',
				'message': u'製作素材失敗：{}'.format(str(e)),
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		#製作素材成功並顯示結果
		response = {
			'status': 'success',
			'message': u'製作素材成功！',
		}
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

def material_update(request, template_name='MaterialADocument/material_update.html', *args, **kwargs):
	if request.method == 'POST':
		materialForm = MaterialForm()
		try:
			m = materialForm.update(request.POST, request.user)
		except TypeError as e:
			return HttpResponseServerError(u'Server Error: 指定的類型不存在')
		except ValueError as e:
			response = {
				'status': 'error',
				'message': u'更新素材失敗',
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		response = {
			'status': 'success',
			'message': u'更新素材成功！',
		}
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

def material_creategroup(request, template_name='MaterialADocument/material_creategroup.html', *args, **kwargs):
	if request.method == 'POST':

		#將POST資料分項存入對應項次的dict
		p=re.compile(r'material-(?P<item>\d+)-(?P<key>.+)')
		main = {}
		data = defaultdict(dict)
		for k,v in request.POST.iteritems():
			search = p.search(k)
			if search:
				data[search.group('item')].update({search.group('key'): v})
			else:
				main.update({k: v})

		#群組素材建立
		materialForm = MaterialForm()
		try:
			main_material = materialForm.create(main, True, request.user)
		except TypeError as e:
			return HttpResponseServerError(u'Server Error: 指定的類型不存在')
		except ValueError as e:
			response = {
				'status': 'error',
				'message': u'製作素材{0}失敗：{1}'.format('main', str(e)),
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		#群組素材的子素材建立
#製作素材失敗需將相關已建立的素材刪除做法
#1. 將群組母素材刪除
#2.群組母素材刪除時，會尋找有關聯的GroupMaterialDetail刪除(models.py)
#3. GroupMaterialDetail刪除時，會尋找有關聯的Material刪除(models.py)

		for k,v in data.iteritems():
			materialForm = MaterialForm()
			try:
				m = materialForm.create(v, True, request.user)
			except TypeError as e:
				main_material[0].delete()
				return HttpResponseServerError(u'Server Error: 指定的類型不存在')
			except ValueError as e:
				main_material[0].delete()
				response = {
					'status': 'error',
					'message': u'製作素材{0}失敗：{1}'.format(k, str(e)),
				}
				return HttpResponse(json.dumps(response), content_type="application/json")

			try:
				mgd = MaterialGroupDetail.objects.create(material_group=main_material[0], material=m[0], seq=int(k))
			except ValidationError as e:
				main_material[0].delete()
				response = {
					'status': 'error',
					'message': u'製作素材{0}失敗：{1}'.format(k, str(e)),
				}
				return HttpResponse(json.dumps(response), content_type="application/json")

		#製作素材成功並顯示結果
		response = {
			'status': 'success',
			'message': u'製作素材成功！',
		}
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

def materialgroup_update_order(request, *args, **kwargs):
	if request.method == 'POST':
		#將POST資料分項存入對應項次的dict
		p=re.compile(r'material-(?P<item>\d+)-(?P<key>.+)')
		main = {}
		data = defaultdict(dict)
		for k,v in request.POST.iteritems():
			search = p.search(k)
			if search:
				data[search.group('item')].update({search.group('key'): v})
			else:
				main.update({k: v})
		main_material = MaterialGroup.objects.get(id=kwargs['id'])

		#重建關聯素材與文件
		mgdAfter = []
		mgdBefore = MaterialGroupDetail.objects.filter(material_group=main_material)
		materialBefore = [material.material for material in mgdBefore]
		materialAfter = []
		try:
			for k,v in data.iteritems():
				exec(
					'material = {0}.objects.get(id={1})'.format(v['type'], v['id'])
				)
				if material.origin_material == False:
					raise ValueError('origin material')

				mgd = MaterialGroupDetail.objects.create(material_group=main_material, material=material, seq=v['seq'])
				mgdAfter.append(mgd)
				materialAfter.append(material)

			#確認是否僅改變順序，素材項目無改變

			import collections
			if not collections.Counter(materialAfter) == collections.Counter(materialBefore):
				raise ValueError('change new item')
		except BaseException as e:
			for i in mgdAfter:
				i.delete()
			response = {
				'status': 'error',
				'message': u'建立文件失敗：{}'.format(str(e)),
			}
			return HttpResponse(content = json.dumps(response), content_type="application/json")

		for i in mgdBefore:
			i.delete_record()
		for i in mgdAfter:
			i.save()

		mgdAfter = MaterialGroupDetail.objects.filter(material_group=main_material)
		materialAfter = [i.material for i in mgdAfter]

		response = {
			'status': 'success',
			'message': u'更新文件成功！',
		}
		return HttpResponse(json.dumps(response), content_type="application/json")

def material_view(request, template_name='MaterialADocument/material_view.html', *args, **kwargs):
	if kwargs['type'] not in ['Text', 'TrueFalse', 'Choice', 'Description', 'MaterialGroup', ]:
		return HttpResponseServerError(u'Server Error: 指定的Material類型不存在')
	if request.method == 'GET' and request.is_ajax():
		exec(
			'material = {0}.objects.get(id={1})'.format(kwargs['type'], kwargs['id'])
		)
		content = material.serialized()
		content.update({'type': kwargs['type']})

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
#				| Q(create_user=None)
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

def material_delete(request, *args, **kwargs):
	if request.method == 'POST':
		try:
			id = int(request.POST['id'])
			exec(
				'material = {0}.objects.get(id=id)'.format(request.POST['type'])
			)
			material.delete()
		except ValueError as e:
			response = {
				'status': 'error',
				'message': u'刪除素材失敗',
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		response = {
			'status': 'success',
			'message': u'刪除素材成功！',
		}
		return HttpResponse(json.dumps(response), content_type="application/json")

def get_form_info(request, template_name='MaterialADocument/get_form_info.html', *args, **kwargs):
	if kwargs['type'] in ['TextForm', 'TrueFalseForm', 'ChoiceForm', 'DescriptionForm', OptionForm, 'MaterialGroupForm', ]:
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
	response = {}
	response['status'] = 'success'
	response['message'] = u''
	response['content'] = field_info

	if request.is_ajax():
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return render(request, template_name, locals())

def document_create(request, template_name='MaterialADocument/document_create.html'):
	if request.method == 'POST':
		#將POST資料分項存入對應項次的dict
		p=re.compile(r'material-(?P<item>\d+)-(?P<key>.+)')
		main = {}
		data = defaultdict(dict)
		for k,v in request.POST.iteritems():
			search = p.search(k)
			if search:
				data[search.group('item')].update({search.group('key'): v})
			else:
				if k == 'topic':
					main.update({k: request.POST.getlist(k)})
				else:
					main.update({k: v})

		documentForm = DocumentForm(main)
		if not documentForm.is_valid():
			response = {
				'status': u'error',
				'message': u'製作文件失敗：{}'.format(str(documentForm.errors))
			}
			return HttpResponse(json.dumps(response), content_type="application/json")
		try:
			main_document = documentForm.save(user=request.user)
		except BaseException as e:
			response = {
				'status': u'error',
				'message': u'製作文件失敗：{}'.format(str(e)),
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		#關聯素材與文件
		try:
			for k,v in data.iteritems():
				exec(
					'material = {0}.objects.get(id={1})'.format(v['type'], v['id'])
				)
				if isinstance(material, Material):
					obj = material.copy_create()
				elif isinstance(material, Document):
					obj = material
				dt = DocumentDetail.objects.create(document=main_document, object=obj, seq=v['seq'])
		except BaseException as e:
			main_document.delete()
			response = {
				'status': 'error',
				'message': u'建立文件失敗：{}'.format(str(e)),
			}
			return HttpResponse(content = json.dumps(response), content_type="application/json")

		response = {
			'status': 'success',
			'message': u'製作文件成功！',
		}
		return HttpResponseRedirect(
			'/',
			content=json.dumps(response),
			content_type="application/json"
		)
	if request.method == 'GET':
		documentForm = DocumentForm()
		return render(request, template_name, locals())

def document_list(request, template_name='MaterialADocument/material_list.html', *args, **kwargs):
	if request.method == 'GET' and request.is_ajax():
		document_list = Document.objects.all()
		content = {}
		for index,material in enumerate(document_list):
			content[index] = material.serialized_abstract()
		response = {
			'status': 'success',
			'message': u'獲取素材{0}列表成功！'.format(kwargs['type']),
			'content': content,
		}
		return HttpResponse(content = json.dumps(response), content_type="application/json")
	elif request.method == 'GET' and not request.is_ajax():
		return render(request, template_name, locals())

def document_update(request, template_name='MaterialADocument/document_update.html', *args, **kwargs):
	if request.method == 'POST':
		main = {}
		for k,v in request.POST.iteritems():
			if k == 'topic':
				main.update({k: request.POST.getlist(k)})
			else:
				main.update({k: v})

		instance=Document.objects.get(id=kwargs['id'])
		documentForm = DocumentForm(main, instance=instance)
		if not documentForm.is_valid():
			response = {
				'status': u'error',
				'message': u'更新文件失敗：{}'.format(str(documentForm.errors))
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		try:
			main_document = documentForm.save(user=request.user)
		except BaseException as e:
			response = {
				'status': u'error',
				'message': u'更新文件失敗：{}'.format(str(e)),
			}
			return HttpResponse(json.dumps(response), content_type="application/json")

		response = {
			'status': 'success',
			'message': u'更新文件成功！',
		}
		return HttpResponse(json.dumps(response), content_type="application/json")
	if request.method == 'GET':
		return render(request, template_name, locals())

def document_update_order(request, *args, **kwargs):
	if request.method == 'POST':
		#將POST資料分項存入對應項次的dict
		p=re.compile(r'material-(?P<item>\d+)-(?P<key>.+)')
		main = {}
		data = defaultdict(dict)
		for k,v in request.POST.iteritems():
			search = p.search(k)
			if search:
				data[search.group('item')].update({search.group('key'): v})
			else:
				main.update({k: v})
		main_document = Document.objects.get(id=kwargs['id'])

		#重建關聯素材與文件
		dtAfter = []
		dtBefore = DocumentDetail.objects.filter(document=main_document)
		materialBefore = [material.object for material in dtBefore]
		materialAfter = []
		try:
			for k,v in data.iteritems():
				exec(
					'material = {0}.objects.get(id={1})'.format(v['type'], v['id'])
				)
				if material.origin_material == True:
					raise ValueError('origin material')

				dt = DocumentDetail.objects.create(document=main_document, object=material, seq=v['seq'])
				dtAfter.append(dt)
				materialAfter.append(material)
			#確認是否僅改變順序，素材項目無改變
			import collections
			if not collections.Counter(materialAfter) == collections.Counter(materialBefore):
				raise ValueError('change new item')
		except BaseException as e:
			for i in dtAfter:
				i.delete_record()
			response = {
				'status': 'error',
				'message': u'建立文件失敗：{}'.format(str(e)),
			}
			return HttpResponse(content = json.dumps(response), content_type="application/json")

		for i in dtBefore:
			i.delete()
		for i in dtAfter:
			i.save()

		response = {
			'status': 'success',
			'message': u'更新文件成功！',
		}
		return HttpResponse(json.dumps(response), content_type="application/json")

def document_view(request, template_name='MaterialADocument/document_view.html', *args, **kwargs):
	if request.method == 'GET' and request.is_ajax():
		document = Document.objects.get(id=kwargs['id'])
		content = document.serialized()

		response = {
			'status': 'success',
			'message': u'獲取文件{0}-{1}成功！'.format(kwargs['type'], kwargs['id']),
			'content': content,
		}
		return HttpResponse(content = json.dumps(response), content_type="application/json")
	elif request.method == 'GET' and not request.is_ajax():
		return render(request, template_name, locals())

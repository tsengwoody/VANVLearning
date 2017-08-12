# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory
from django.utils import timezone

from MaterialADocument.models import *
from MaterialADocument.tests_data import *
from users.models import *


class Command(BaseCommand):
	help = 'initial database'
	def add_arguments(self, parser):
		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'root firstname', last_name = 'root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2017-01-01')
		root.set_password('root')
#		root.status = root.STATUS['active']
		root.auth_email = True
		root.auth_phone = True
		root.save()
		Subject.objects.create(name=u'國中數學(課綱)')
		Subject.objects.create(name=u'國中數學(自訂)')
		s = Subject.objects.create(name=u'高中數學(課綱)')
		s2 = Subject.objects.create(name=u'高中數學(自訂)')
		Subject.objects.create(name=u'線性代數')
		Topic.objects.create(subject=s, name=u'實數')
		Topic.objects.create(subject=s, name=u'絕對值')
		Topic.objects.create(subject=s, name=u'指數')
		Topic.objects.create(subject=s2, name=u'微積分')

#	def test_correct_Text_case(self):
		client = Client()
		client.login(username='root', password='root')
		previous_count = len(Text.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_create'),
			Text1_data,
		)
		assert len(Text.objects.all()) == previous_count + 1, 'Text create failed'

#	def test_correct_Text_case2(self):
		previous_count = len(Text.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_create'),
			Text2_data,
		)
		assert len(Text.objects.all()) == previous_count + 1, 'Text create failed'

#type:　TrueFalse

#	def test_correct_TrueFalse_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse1_data,
		)
		assert len(TrueFalse.objects.all()) == previous_count + 1, 'TrueFalse create failed'

#	def test_correct_TrueFalse_case2(self):
		previous_count = len(TrueFalse.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse1_data,
		)
		assert len(TrueFalse.objects.all()) == previous_count + 1, 'TrueFalse create failed'

#Type:　Choice

#	def test_correct_Choice_case(self):
		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_create'),
			Choice1_data,
		)
		assert len(Choice.objects.all()) == previous_count + 1, 'choices create failed'
		assert len(Option.objects.all()) == previous_option_count + 4, 'option create failed'

#Type = MaterialGroup

#	def test_correct_materialgroup_case(self):
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_creategroup'),
			MaterialGroup1_data
		)
		assert len(MaterialGroup.objects.all())== previous_materialgroup_count + 1
		assert len(Choice.objects.all())== previous_choice_count + 4
		assert len(Option.objects.all())== previous_option_count + 16
		assert len(Description.objects.all())== previous_description_count + 1
		assert len(MaterialGroupDetail.objects.all())== previous_materialgroupdetail_count + 5
		assert response.json()['status'] == 'success'

#	def test_correct_materialgroup_case2(self):
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = client.post(
			reverse('MaterialADocument:material_creategroup'),
			MaterialGroup2_data,
		)
		assert len(MaterialGroup.objects.all())== previous_materialgroup_count + 1
		assert len(Choice.objects.all())== previous_choice_count + 4
		assert len(Option.objects.all())== previous_option_count + 16
		assert len(Description.objects.all())== previous_description_count + 1
		assert len(MaterialGroupDetail.objects.all())== previous_materialgroupdetail_count + 5
		assert response.json()['status'] == 'success'
		previous_count = len(Document.objects.all())
		previous_TrueFalse_count = len(TrueFalse.objects.all())
		response = client.post(
			reverse('MaterialADocument:document_create'),
			{
				'type': '0',
				'subject': '3',
				'topic': ['1', '2'],
				'privacy': '2',
				'title': u'二元一次方程式解',
				'abstract': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
				'material-0-type': 'TrueFalse',
				'material-0-id': '1',
				'material-0-seq': '1',
				'material-1-type': 'TrueFalse',
				'material-1-id': '2',
				'material-1-seq': '2',
			},
		)
		assert response.json()['status'] == 'success'
		assert len(Document.objects.all()) == previous_count + 1
		assert len(TrueFalse.objects.all()) == previous_TrueFalse_count + 2

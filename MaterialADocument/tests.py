# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase

from MaterialADocument.models import *

class material_createViewTests(TestCase):

	@classmethod
	def setUpClass(cls):
		super(material_createViewTests, cls).setUpClass()
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'root firstname', last_name = 'root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2017-01-01')
		root.set_password('root')
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

	def test_correct_TrueFalse_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse(
			'MaterialADocument:material_create'),
			{
				'type': 'TrueFalse',
				'subject': '3',
				'topic': '1',
				'privacy': '2',
				'title': '二元一次方程式解',
				'answer': 'True',
			},
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)
		trueFalse = TrueFalse.objects.first()
		

	def test_error_type_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse(
			'MaterialADocument:material_create'),
			{
				'type': 'trueFalse',
				'subject': '3',
				'topic': '1',
				'privacy': '2',
				'title': '二元一次方程式解',
				'answer': 'True',
			},
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

	def test_error_SubjectToTopic_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse(
			'MaterialADocument:material_create'),
			{
				'type': 'TrueFalse',
				'subject': '2',
				'topic': '1',
				'privacy': '2',
				'title': '二元一次方程式解',
				'answer': 'True',
			},
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)


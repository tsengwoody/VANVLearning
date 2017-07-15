﻿# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase

from MaterialADocument.forms import *
from MaterialADocument.models import *

EMPTY_OPTION = ([u'', u'---------'],)

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
		#合法subject:type
		#3:1, 3:2, 3:3, 4:4

	def test_correct_Text_case(self):
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'Text',
				'subject': '4',
				'topic': '4',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		self.assertEqual(len(Text.objects.all()), previous_count + 1)

	def test_correct_TrueFalse_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'TrueFalse',
				'subject': '3',
				'topic': '1',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'answer': 'True',
			},
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)

	def test_correct_Choice_case(self):
		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'Choice',
				'subject': '4',
				'topic': '4',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'form-TOTAL_FORMS': '2',
				'form-INITIAL_FORMS': '0',
				'form-MAX_NUM_FORMS': '10',
				'form-0-content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
				'form-0-is_answer': 'True',
				'form-1-content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>b</mi></mrow></mfrac></mrow></math>',
				'form-1-is_answer': 'False',
			},
		)
		self.assertEqual(len(Choice.objects.all()), previous_count + 1)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 2)

	def test_correct_Description_case(self):
		previous_count = len(Description.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'Description',
				'subject': '3',
				'topic': '2',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'answer': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		self.assertEqual(len(Description.objects.all()), previous_count + 1)

	def test_correct_redirect_case(self):
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'Text',
				'subject': '4',
				'topic': '4',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		m = Text.objects.first()
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, reverse('MaterialADocument:material_view', kwargs={
			'type': m.__class__.__name__,
			'id': m.id,
		}, ))

	def test_error_type_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'trueFalse',
				'subject': '3',
				'topic': '1',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'answer': 'True',
			},
		)
		self.assertEqual(response.status_code, 500)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

	def test_error_SubjectToTopic_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			{
				'type': 'TrueFalse',
				'subject': '2',
				'topic': '1',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'answer': 'True',
			},
		)
		self.assertEqual(response.json()['status'], 'error')
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

class get_form_infoViewTests(TestCase):

	@classmethod
	def setUpClass(cls):
		super(get_form_infoViewTests, cls).setUpClass()
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

	def test_correct_Text_case(self):
		response = self.client.get(
			reverse('MaterialADocument:get_form_info', kwargs={'type': 'TextForm', }, ),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		subject_choices = list(EMPTY_OPTION) + [[subject.id, subject.name] for subject in Subject.objects.all()]
		self.assertEqual(response.json()['0']['choices'], subject_choices)
		SubjectToTopic = {}
		for subject in Subject.objects.all():
			SubjectToTopic[unicode(subject.id)] = [[topic.id, topic.name] for topic in subject.topic_set.all()]
		self.assertEqual(response.json()['SubjectToTopic'], SubjectToTopic)

	def test_error_type_case(self):
		response = self.client.get(
			reverse('MaterialADocument:get_form_info', kwargs={'type': 'textForm', }, ),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(response.status_code, 500)

class material_creategroupViewTests(TestCase):

	@classmethod
	def setUpClass(cls):
		super(material_creategroupViewTests, cls).setUpClass()
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
		#合法subject:type
		#3:1, 3:2, 3:3, 4:4

	def test_correct_2items_case(self):
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_creategroup'),
			{
				'material_count': '2',
				'type': 'MaterialGroup',
				'subject': '4',
				'topic': '4',
				'privacy': '2',
				'title': u'二元一次方程式解群組題',
				'content': u'群組素材內容',
				'material-0-type': 'Choice',
				'material-0-subject': '4',
				'material-0-topic': '4',
				'material-0-privacy': '2',
				'material-0-title': u'二元一次方程式解',
				'material-0-form-TOTAL_FORMS': '2',
				'material-0-form-INITIAL_FORMS': '0',
				'material-0-form-MAX_NUM_FORMS': '10',
				'material-0-form-0-content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
				'material-0-form-0-is_answer': 'True',
				'material-0-form-1-content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>b</mi></mrow></mfrac></mrow></math>',
				'material-0-form-1-is_answer': 'False',
				'material-1-type': 'Description',
				'material-1-subject': '4',
				'material-1-topic': '4',
				'material-1-privacy': '2',
				'material-1-title': u'二元一次方程式解問答題',
				'material-1-answer': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		self.assertEqual(len(MaterialGroup.objects.all()), previous_materialgroup_count + 1)
		self.assertEqual(len(Choice.objects.all()), previous_choice_count + 1)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 2)
		self.assertEqual(len(Description.objects.all()), previous_description_count + 1)
		self.assertEqual(len(MaterialGroupDetail.objects.all()), previous_materialgroupdetail_count + 2)
		m = MaterialGroup.objects.first()
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, reverse('MaterialADocument:material_view', kwargs={
			'type': m.__class__.__name__,
			'id': m.id,
		}, ))

	def test_error_material_no_match_materialgroup_data_case(self):
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_creategroup'),
			{
				'material_count': '2',
				'type': 'MaterialGroup',
				'subject': '4',
				'topic': '4',
				'privacy': '2',
				'title': u'二元一次方程式解群組題',
				'content': u'群組素材內容',
				'material-0-type': 'Choice',
				'material-0-subject': '4',
				'material-0-topic': '1',
				'material-0-privacy': '1',
				'material-0-title': u'二元一次方程式解',
				'material-0-form-TOTAL_FORMS': '2',
				'material-0-form-INITIAL_FORMS': '0',
				'material-0-form-MAX_NUM_FORMS': '10',
				'material-0-form-0-content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
				'material-0-form-0-is_answer': 'True',
				'material-0-form-1-content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>b</mi></mrow></mfrac></mrow></math>',
				'material-0-form-1-is_answer': 'False',
				'material-1-type': 'Description',
				'material-1-subject': '4',
				'material-1-topic': '4',
				'material-1-privacy': '2',
				'material-1-title': u'二元一次方程式解問答題',
				'material-1-answer': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		#待處理
		self.assertEqual(len(MaterialGroup.objects.all()), previous_materialgroup_count)
		self.assertEqual(len(Choice.objects.all()), previous_choice_count)
		self.assertEqual(len(Option.objects.all()), previous_option_count)
		self.assertEqual(len(Description.objects.all()), previous_description_count)
		self.assertEqual(len(MaterialGroup.objects.all()), previous_materialgroup_count)
		self.assertEqual(len(MaterialGroupDetail.objects.all()), previous_materialgroupdetail_count)

class material_viewViewTests(TestCase):

	@classmethod
	def setUpClass(cls):
		super(material_viewViewTests, cls).setUpClass()
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
		#合法subject:type
		#3:1, 3:2, 3:3, 4:4
		materialForm = MaterialForm()
		data = {
			'type': 'Text',
			'subject': '4',
			'topic': '4',
			'privacy': '2',
			'title': u'二元一次方程式解',
			'content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
		}
		user = User.objects.get(username='root')
		m = materialForm.fill(data, True, user)

	def test_correct_Text_case(self):
		response = self.client.get(
			reverse(
				'MaterialADocument:material_view',
				kwargs = {
					'type': 'Text',
					'id': '1',
				},
			),
		)

class material_listViewTests(TestCase):

	def setUp(self):
		super(material_listViewTests, self).setUpClass()
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'root firstname', last_name = 'root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2017-01-01')
		root.set_password('root')
		root.auth_email = True
		root.auth_phone = True
		root.save()
		self.client.login(username='root', password='root')
		Subject.objects.create(name=u'國中數學(課綱)')
		Subject.objects.create(name=u'國中數學(自訂)')
		s = Subject.objects.create(name=u'高中數學(課綱)')
		s2 = Subject.objects.create(name=u'高中數學(自訂)')
		Subject.objects.create(name=u'線性代數')
		Topic.objects.create(subject=s, name=u'實數')
		Topic.objects.create(subject=s, name=u'絕對值')
		Topic.objects.create(subject=s, name=u'指數')
		Topic.objects.create(subject=s2, name=u'微積分')
		#合法subject:type
		#3:1, 3:2, 3:3, 4:4
		materialForm = MaterialForm()
		data = {
			'type': 'Text',
			'subject': '4',
			'topic': '4',
			'privacy': '2',
			'title': u'二元一次方程式解',
			'content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
		}
		user = User.objects.get(username='root')
		m = materialForm.fill(data, True, user)
		data = {
			'type': 'Text',
			'subject': '4',
			'topic': '4',
			'privacy': '2',
			'title': u'二元一次方程式解',
			'content': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
		}
		user = User.objects.get(username='root')
		m = materialForm.fill(data, True, user)
		data = 			{
			'type': 'TrueFalse',
			'subject': '3',
			'topic': '1',
			'privacy': '2',
			'title': u'二元一次方程式解',
			'answer': 'True',
		}
		m = materialForm.fill(data, True, user)

	def test_correct_Text_case(self):
		response = self.client.get(
			reverse(
				'MaterialADocument:material_list',
				kwargs = {
					'type': 'Text',
				},
			),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(response.json()['status'], 'success')
		self.assertEqual(response.json()['content']['0'], Text.objects.get(id=1).serialized_abstract())
		self.assertEqual(response.json()['content']['1'], Text.objects.get(id=2).serialized_abstract())

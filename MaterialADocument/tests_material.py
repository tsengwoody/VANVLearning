# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase

from MaterialADocument.forms import *
from MaterialADocument.models import *
from MaterialADocument.tests_data import *

EMPTY_OPTION = ([u'', u'---------'],)

class material_createViewTests(basedSetup):
	def setUp(self):
		super(material_createViewTests, self).setUp()

	def test_correct_Text_case(self):
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Text1_data,
		)
		self.assertEqual(len(Text.objects.all()), previous_count + 1)

	def test_correct_TrueFalse_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse1_data,
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)

	def test_correct_Choice_case(self):
		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Choice1_data,
		)
		self.assertEqual(len(Choice.objects.all()), previous_count + 1)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 4)

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
			Choice2_data,
		)
		m = Choice.objects.first()
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, reverse('MaterialADocument:material_view', kwargs={
			'type': m.__class__.__name__,
			'id': m.id,
		}, ))
#		print response['Location']

	def test_error_type_case(self):
		previous_count = len(TrueFalse.objects.all())
		data = Text1_data.copy()
		data.update({'type': 'trueFalse',})
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			data,
		)
		self.assertEqual(response.status_code, 500)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

	def test_error_SubjectToTopic_case(self):
		previous_count = len(TrueFalse.objects.all())
		data = Text1_data.copy()
		data.update({'subject': '2',})
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			data,
		)
		self.assertEqual(response.json()['status'], 'error')
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

class material_updateViewTests(basedSetupMaterial):
	def setUp(self):
		super(material_updateViewTests, self).setUp()

	def test_correct_Text_case(self):
		previous_count = len(Text.objects.all())
		data = Text1_data.copy()
		data.update({
			'id': '1',
			'privacy': '0',
		})
		response = self.client.post(
			reverse(
				'MaterialADocument:material_update',
				kwargs = {
					'type': 'Text',
					'id': '1',
				},
			),
			data,
		)
		text = Text.objects.get(id=1)
		self.assertEqual(text.privacy, 0)
		self.assertEqual(len(Text.objects.all()), previous_count)

	def test_correct_TrueFalse_case(self):
		previous_count = len(TrueFalse.objects.all())
		data = TrueFalse1_data.copy()
		data.update({
			'id': '1',
			'privacy': '0',
		})
		response = self.client.post(
			reverse(
				'MaterialADocument:material_update',
				kwargs = {
					'type': 'Text',
					'id': '1',
				},
			),
			data,
		)
		TF = TrueFalse.objects.get(id=1)
		self.assertEqual(TF.privacy, 0)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

	def test_correct_Choice_case(self):
		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = self.client.post(
			reverse(
				'MaterialADocument:material_update',
				kwargs = {
					'type': 'Text',
					'id': '1',
				},
			),
			{
				'id': '1',
				'type': 'Choice',
				'subject': '4',
				'topic': '4',
				'privacy': '2',
				'title': u'在一容器中有A、B兩種菌﹐且在任何時刻這兩種菌的個數乘積為一定值<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>8</mn></msup></math>。若以<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mo>=</mo><mi>log</mi><mo>(</mo><msub><mi>n</mi><mi>A</mi></msub><mo>)</mo><mspace linebreak="newline"/></math>來記錄A菌個數的資料﹐其中<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>n</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>為 A 菌的個數﹐則下列哪些選項是正確的？',
				'form-TOTAL_FORMS': '3',
				'form-INITIAL_FORMS': '0',
			#	'form-MAX_NUM_FORMS': '10',
				'form-0-content': u'<math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1</mn><mo>&#x2264;</mo><msub><mi>P</mi><mi>A</mi></msub><mo>&#x2264;</mo><mn>8</mn><mspace linebreak="newline"/></math>',
				'form-0-is_answer': 'False',
				'form-1-content': u'當<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mo>=</mo><mn>4</mn><mspace linebreak="newline"/></math>時﹐B 菌的個數與A菌的個數相同',
				'form-1-is_answer': 'True',	
				'form-2-content': u'如果上週一測得<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>值為 2 而上週五測得<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>值為 4﹐表示上週五 A 菌的個數是上週一 A 菌個數的2倍',
				'form-2-is_answer': 'False',	
			}
		)
		self.assertEqual(len(Choice.objects.all()), previous_count)
		self.assertEqual(len(Option.objects.all()), previous_option_count-1)

	def test_correct_Description_case(self):
		previous_count = len(Description.objects.all())
		response = self.client.post(
			reverse(
				'MaterialADocument:material_update',
				kwargs = {
					'type': 'Text',
					'id': '1',
				},
			),
			{
				'id': '1',
				'type': 'Description',
				'subject': '3',
				'topic': '2',
				'privacy': '2',
				'title': u'二元一次方程式解',
				'answer': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		self.assertEqual(len(Description.objects.all()), previous_count)

	def test_error_unchange_field_case(self):
		previous_count = len(TrueFalse.objects.all())
		data = TrueFalse1_data.copy()
		data.update({
			'id': '1',
			'subject': '4',
				'topic': '4',
		})
		response = self.client.post(
			reverse(
				'MaterialADocument:material_update',
				kwargs = {
					'type': 'Text',
					'id': '1',
				},
			),
			data,
		)
		TF = TrueFalse.objects.get(id=1)
		self.assertEqual(TF.topic, Topic.objects.get(id=1))
		self.assertEqual(len(TrueFalse.objects.all()), previous_count)

class material_deleteViewTests(basedSetupMaterial):

	def setUp(self):
		super(material_deleteViewTests, self).setUp()

	def test_correct_case(self):
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_delete'),
			{
				'type': 'Text',
				'id': '1',
			},
		)
		self.assertEqual(len(Text.objects.all()), previous_count - 1)

class get_form_infoViewTests(basedSetup):
	def setUp(self):
		super(get_form_infoViewTests, self).setUpClass()

	def test_correct_Text_case(self):
		response = self.client.get(
			reverse('MaterialADocument:get_form_info', kwargs={'type': 'TextForm', }, ),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		subject_choices = list(EMPTY_OPTION) + [[subject.id, subject.name] for subject in Subject.objects.all()]
		self.assertEqual(response.json()['content']['0']['choices'], subject_choices)
		SubjectToTopic = {}
		for subject in Subject.objects.all():
			SubjectToTopic[unicode(subject.id)] = [[topic.id, topic.name] for topic in subject.topic_set.all()]
		self.assertEqual(response.json()['content']['SubjectToTopic'], SubjectToTopic)

	def test_error_type_case(self):
		response = self.client.get(
			reverse('MaterialADocument:get_form_info', kwargs={'type': 'textForm', }, ),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(response.status_code, 500)

class material_creategroupViewTests(basedSetup):
	def setUp(self):
		super(material_creategroupViewTests, self).setUp()

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
#				'material-0-form-MAX_NUM_FORMS': '10',
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

class material_viewViewTests(basedSetup):

	def setUp(self):
		super(material_viewViewTests, self).setUp()

		materialForm = MaterialForm()
		user = User.objects.get(username='root')
		m = materialForm.create(Text1_data, True, user)

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

class material_listViewTests(basedSetup):
	def setUp(self):
		super(material_listViewTests, self).setUp()
		materialForm = MaterialForm()
		user = User.objects.get(username='root')
		m = materialForm.create(Text1_data, True, user)
		m = materialForm.create(Text2_data, True, user)
		m = materialForm.create(TrueFalse1_data, True, user)

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

class material_createViewTests2(basedSetup):
	def setUp(self):
		super(material_createViewTests2, self).setUp()

	def test_correct_Text_case(self):
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Text1_data,
		)
		self.assertEqual(len(Text.objects.all()), previous_count + 1)

	def test_correct_Text_case2(self):
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Text2_data,
		)
		self.assertEqual(len(Text.objects.all()), previous_count + 1)

	def test_correct_TrueFalse_case(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse1_data,
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)

	def test_correct_TrueFalse_case2(self):
		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse2_data,
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)

	def test_correct_Choice_case(self):
		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Choice1_data,
		)
		self.assertEqual(len(Choice.objects.all()), previous_count + 1)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 4)

	def test_correct_Choice_case2(self):
		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Choice2_data,
		)
		self.assertEqual(len(Choice.objects.all()), previous_count + 1)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 4)

	def test_correct_materialgroup_case(self):
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_creategroup'),
			MaterialGroup1_data,
		)
		self.assertEqual(len(MaterialGroup.objects.all()), previous_materialgroup_count + 1)
		self.assertEqual(len(Choice.objects.all()), previous_choice_count + 4)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 16)
		self.assertEqual(len(Description.objects.all()), previous_description_count + 1)
		self.assertEqual(len(MaterialGroupDetail.objects.all()), previous_materialgroupdetail_count + 5)
		m = MaterialGroup.objects.first()
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, reverse('MaterialADocument:material_view', kwargs={
			'type': m.__class__.__name__,
			'id': m.id,
		},))

	def test_correct_materialgroup_case2(self):
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_creategroup'),
			MaterialGroup3_data,
		)
		self.assertEqual(len(MaterialGroup.objects.all()), previous_materialgroup_count + 1)
		self.assertEqual(len(Choice.objects.all()), previous_choice_count + 4)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 16)
#		self.assertEqual(len(Description.objects.all()), previous_description_count + 1)
		self.assertEqual(len(MaterialGroupDetail.objects.all()), previous_materialgroupdetail_count + 4)
		m = MaterialGroup.objects.first()
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, reverse('MaterialADocument:material_view', kwargs={
			'type': m.__class__.__name__,
			'id': m.id,
		}, ))

class material_updateViewTests(basedSetupMaterial):
	def setUp(self):
		super(material_updateViewTests, self).setUp()

	def test_correct_material_update_order_Text_case(self):
		materialGroup = MaterialGroup.objects.get(id=1)
		mgd = MaterialGroupDetail.objects.filter(material_group=materialGroup)
		materialBefore = [i.material for i in mgd]
		data = {}
		for index, material in enumerate(materialBefore):
			data.update({
				'material-{0}-type'.format(index): material.__class__.__name__,
				'material-{0}-id'.format(index): material.id,
				'material-{0}-seq'.format(index): str(index),
			})
		response = self.client.post(
			reverse(
				'MaterialADocument:materialgroup_update_order',
				kwargs = {
					'id': '1',
				},
			),
			data,
		)
#		print response.json()['message']
		self.assertEqual(response.json()['status'], 'success')
		mgd = MaterialGroupDetail.objects.filter(material_group=materialGroup)
		materialAfter = [i.material for i in mgd]
		import collections
		self.assertTrue(collections.Counter(materialAfter) == collections.Counter(materialBefore))
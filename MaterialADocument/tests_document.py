# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase

from MaterialADocument.forms import *
from MaterialADocument.models import *
from MaterialADocument.tests_data import *

class document_createViewTests(basedSetupMaterial):
	def setUp(self):
		super(document_createViewTests, self).setUp()

	def test_correct_Text_case(self):
		previous_count = len(Document.objects.all())
		previous_TrueFalse_count = len(TrueFalse.objects.all())
		response = self.client.post(
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
#		print response.json()['message']
		self.assertEqual(response.json()['status'], 'success')
		self.assertEqual(len(Document.objects.all()), previous_count + 1)
		self.assertEqual(len(TrueFalse.objects.all()), previous_TrueFalse_count + 2)

class document_updateViewTests(basedSetupDocument):
	def setUp(self):
		super(document_updateViewTests, self).setUp()

	def test_correct_document_update_Text_case(self):
		previous_count = len(Document.objects.all())
		response = self.client.post(
			reverse(
				'MaterialADocument:document_update',
				kwargs = {
					'id': '1',
				},
			),
			{
				'type': '0',
				'subject': '3',
				'topic': ['1', '2', '3'],
				'privacy': '2',
				'title': u'二元一次方程式解',
				'abstract': u'<math><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo form="prefix">−</mo><mi>b</mi><mo>&PlusMinus;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mo>&InvisibleTimes;</mo><mi>a</mi><mo>&InvisibleTimes;</mo><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>a</mi></mrow></mfrac></mrow></math>',
			},
		)
		self.assertEqual(response.json()['status'], 'success')
		self.assertEqual(len(Document.objects.all()), previous_count)

	def test_correct_document_update_order_Text_case(self):
		document = Document.objects.get(id=1)
		material3 = TrueFalse.objects.get(id=3)
		material4 = TrueFalse.objects.get(id=4)
		dt = DocumentDetail.objects.filter(document=document)
		for i in dt:
			if i.object == material3:
				self.assertEqual(i.seq,1)
			if i.object == material4:
				self.assertEqual(i.seq,0)
		response = self.client.post(
			reverse(
				'MaterialADocument:document_update_order',
				kwargs = {
					'id': '1',
				},
			),
			{
				'material-0-type': 'TrueFalse',
				'material-0-id': '3',
				'material-0-seq': '0',
				'material-1-type': 'TrueFalse',
				'material-1-id': '4',
				'material-1-seq': '1',
			},
		)
		self.assertEqual(response.json()['status'], 'success')
		dt = DocumentDetail.objects.filter(document=document)
		for i in dt:
			if i.object == material3:
				self.assertEqual(i.seq,0)
			if i.object == material4:
				self.assertEqual(i.seq,1)
		self.assertEqual(response.json()['status'], 'success')

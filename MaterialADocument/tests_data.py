# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase

from MaterialADocument.forms import *
from MaterialADocument.models import *

Text1_data = {
	'type': 'Text',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'園遊會時，一年十九班賣雞排與珍珠奶茶，賣一塊雞排賺 15 元，賣一杯珍珠奶茶賺 10 元，最後總共賺 850 元，若賣出雞排 x 塊、珍珠奶茶 y 杯，請列出符合題意的方程式',
	'content': u'<math xmlns="http://www.w3.org/1998/Math/MathML"><mn>15</mn><mi>x</mi><mo>+</mo><mn>10</mn><mi>y</mi><mo>=</mo><mn>850</mn><mspace linebreak="newline"/><mspace linebreak="newline"/></math>',
}

Text2_data = {
	'type': 'Text',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'某二位數的個位數字為a，已知十位數字比個位數字大4，則此二位數可表示為？',
	'content': u'<math xmlns="http://www.w3.org/1998/Math/MathML"><mn>10</mn><mo>(</mo><mi>a</mi><mo>+</mo><mn>4</mn><mo>)</mo><mo>+</mo><mi>a</mi><mspace linebreak="newline"/><mspace linebreak="newline"/></math>',
}

TrueFalse1_data = {
	'type': 'TrueFalse',
	'subject': '3',
	'topic': '1',
	'privacy': '2',
	'title': u'甲、乙、丙三人並坐一排，已知任意兩人的年齡和分別為 63、69、78，則三人中年齡最大的為78歲',
	'answer': 'True',
}

TrueFalse2_data = {
	'type': 'TrueFalse',
	'subject': '3',
	'topic': '1',
	'privacy': '2',
	'title': u'某班 45 位學生，其中男生 x 位，女生 y 位， 若男生的平均分數是 80 分，女生的平均分數是 75 分， 且全班的平均分數是 78 分，則解出男生有18位，女生27位 ',
	'answer': 'False',
}

Choice1_data = {
	'type': 'Choice',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'在一容器中有A、B兩種菌﹐且在任何時刻這兩種菌的個數乘積為一定值<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>8</mn></msup></math>。若以<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mo>=</mo><mi>log</mi><mo>(</mo><msub><mi>n</mi><mi>A</mi></msub><mo>)</mo><mspace linebreak="newline"/></math>來記錄A菌個數的資料﹐其中<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>n</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>為 A 菌的個數﹐則下列哪些選項是正確的？',
	'form-TOTAL_FORMS': '4',
	'form-INITIAL_FORMS': '0',
#	'form-MAX_NUM_FORMS': '10',
	'form-0-content': u'<math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1</mn><mo>&#x2264;</mo><msub><mi>P</mi><mi>A</mi></msub><mo>&#x2264;</mo><mn>8</mn><mspace linebreak="newline"/></math>',
	'form-0-is_answer': 'False',
	'form-1-content': u'當<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mo>=</mo><mn>4</mn><mspace linebreak="newline"/></math>時﹐B 菌的個數與A菌的個數相同',
	'form-1-is_answer': 'True',	
	'form-2-content': u'如果上週一測得<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>值為 2 而上週五測得<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>值為 4﹐表示上週五 A 菌的個數是上週一 A 菌個數的2倍',
	'form-2-is_answer': 'False',	
	'form-3-content': u'若今天的<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>P</mi><mi>A</mi></msub><mspace linebreak="newline"/></math>值比昨天增加 1﹐則今天的 A 菌個數為昨天的 2 倍',
	'form-3-is_answer': 'False',
}

Choice2_data = {
	'type': 'Choice',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'下列對數﹐首數為<math xmlns="http://www.w3.org/1998/Math/MathML"><mo>-</mo><mn>3</mn><mspace linebreak="newline"/></math>的是：',
	'form-TOTAL_FORMS': '4',
	'form-INITIAL_FORMS': '0',
#	'form-MAX_NUM_FORMS': '10',
	'form-0-content': u'log0.0023',
	'form-0-is_answer': 'True',
	'form-1-content': u'log0.00023',
	'form-1-is_answer': 'False',	
	'form-2-content': u'<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>log</mi><mfrac><mn>1</mn><mn>123</mn></mfrac><mspace linebreak="newline"/></math>',
	'form-2-is_answer': 'True',	
	'form-3-content': u'<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>log</mi><mi>a</mi><mo>&#xA0;</mo><mo>&#x2248;</mo><mo>&#xA0;</mo><mo>-</mo><mn>3</mn><mo>.</mo><mn>4771</mn><mspace linebreak="newline"/></math>',
	'form-3-is_answer': 'False',
}

MaterialGroup1_data = {
	'material_count': '2',
	'type': 'MaterialGroup',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'英文語意群組題-The uncanny valley-1',
	'content': u"The most popular social-networking phenomenon, Facebook, may now hide some dangers. Facebook's signup procedure asks for a lot of personal information which will __1__ the data of other users together on a server. __2__, according to the statistics, 72 percent of users reveal their email address; 84 percent provide their date of birth; 78 percent give their address; 23 percent __3__ their phone number. Some people even disclose their mothers’ maiden names often used as a secret password to access a financial account. __4__ our unwillingness to share this kind of privacy with someone we meet in real life, interestingly we're quite contented to give it to a total stranger online. We must know that no matter how hard the sites try to guard your information, the potential for identity theft is disturbing. You must protect the personal data __5__ it were a matter of life and death, and don’t rely on anyone else.",
	'material-0-type': 'Choice',
	'material-0-subject': '4',
	'material-0-topic': '4',
	'material-0-privacy': '2',
	'material-0-title': u'choose the correct answer',
	'material-0-form-TOTAL_FORMS': '4',
	'material-0-form-INITIAL_FORMS': '0',
#	'material-0-form-MAX_NUM_FORMS': '10',
	'material-0-form-0-content': u'present',
	'material-0-form-0-is_answer': 'False',
	'material-0-form-1-content': u'join',
	'material-0-form-1-is_answer': 'True',
	'material-0-form-2-content': u'locate',
	'material-0-form-2-is_answer': 'False',
	'material-0-form-3-content': u'circulate',
	'material-0-form-3-is_answer': 'False',
	'material-1-type': 'Choice',
	'material-1-subject': '4',
	'material-1-topic': '4',
	'material-1-privacy': '2',
	'material-1-title': u'choose the correct answer',
	'material-1-form-TOTAL_FORMS': '4',
	'material-1-form-INITIAL_FORMS': '0',
#	'material-1-form-MAX_NUM_FORMS': '10',
	'material-1-form-0-content': u'Even so',
	'material-1-form-0-is_answer': 'False',
	'material-1-form-1-content': u'by contrast',
	'material-1-form-1-is_answer': 'False',
	'material-1-form-2-content': u'In effect',
	'material-1-form-2-is_answer': 'True',
	'material-1-form-3-content': u'all in all',
	'material-1-form-3-is_answer': 'False',
	'material-2-type': 'Description',
	'material-2-subject': '4',
	'material-2-topic': '4',
	'material-2-privacy': '2',
	'material-2-title': u'fill the correct answer',
	'material-2-answer': u'state',
	'material-3-type': 'Choice',
	'material-3-subject': '4',
	'material-3-topic': '4',
	'material-3-privacy': '2',
	'material-3-title': u'choose the correct answer',
	'material-3-form-TOTAL_FORMS': '4',
	'material-3-form-INITIAL_FORMS': '0',
#	'material-3-form-MAX_NUM_FORMS': '10',
	'material-3-form-0-content': u'For all',
	'material-3-form-0-is_answer': 'True',
	'material-3-form-1-content': u'Owing',
	'material-3-form-1-is_answer': 'False',
	'material-3-form-2-content': u'Expect for',
	'material-3-form-2-is_answer': 'False',
	'material-3-form-3-content': u'let alone',
	'material-3-form-3-is_answer': 'False',
	'material-4-type': 'Choice',
	'material-4-subject': '4',
	'material-4-topic': '4',
	'material-4-privacy': '2',
	'material-4-title': u'choose the correct answer',
	'material-4-form-TOTAL_FORMS': '4',
	'material-4-form-INITIAL_FORMS': '0',
#	'material-4-form-MAX_NUM_FORMS': '10',
	'material-4-form-0-content': u'Seeing that',
	'material-4-form-0-is_answer': 'False',
	'material-4-form-1-content': u'as long as',
	'material-4-form-1-is_answer': 'False',
	'material-4-form-2-content': u'as if',
	'material-4-form-2-is_answer': 'True',
	'material-4-form-3-content': u'lest',
	'material-4-form-3-is_answer': 'False',
}

MaterialGroup2_data = {
	'material_count': '2',
	'type': 'MaterialGroup',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'英文語意群組題-The uncanny valley-2',
	'content': u"Most people are aware that it is very important to make sure that fruits are parts of your diet. Most fruits are full of vitamins A and C and are almost __1__ fat. However, there are a few fruits that are either insufficient in certain __2__ or are exaggerated too much in their benefits. First, almost all fruits are low __3__ calories, but apples and bananas are the ones that are at 100 calories or above. Second, you should never have put an avocado or olive on your fruit salad because of their high fat content. Third, blueberries and cranberries contain no vitamin A. Furthermore, most of the fruits are very good sources of vitamin C, __4__ grapes and apples which only have merely 5 percent. Last but not the least, almost half of all fruits contains less than 1 percent of the recommended daily allowance of calcium or iron. In conclusion, since fruits are necessary, make sure that you choose the right __5__ benefit you the best.",
	'material-0-type': 'Choice',
	'material-0-subject': '4',
	'material-0-topic': '4',
	'material-0-privacy': '2',
	'material-0-title': u'choose the correct answer',
	'material-0-form-TOTAL_FORMS': '4',
	'material-0-form-INITIAL_FORMS': '0',
#	'material-0-form-MAX_NUM_FORMS': '10',
	'material-0-form-0-content': u'free of',
	'material-0-form-0-is_answer': 'True',
	'material-0-form-1-content': u'far from',
	'material-0-form-1-is_answer': 'False',
	'material-0-form-2-content': u'in exchange for',
	'material-0-form-2-is_answer': 'False',
	'material-0-form-3-content': u'at the expense of',
	'material-0-form-3-is_answer': 'False',
	'material-1-type': 'Choice',
	'material-1-subject': '4',
	'material-1-topic': '4',
	'material-1-privacy': '2',
	'material-1-title': u'choose the correct answer',
	'material-1-form-TOTAL_FORMS': '4',
	'material-1-form-INITIAL_FORMS': '0',
#	'material-1-form-MAX_NUM_FORMS': '10',
	'material-1-form-0-content': u'departments',
	'material-1-form-0-is_answer': 'False',
	'material-1-form-1-content': u'definitions',
	'material-1-form-1-is_answer': 'False',
	'material-1-form-2-content': u'categories',
	'material-1-form-2-is_answer': 'True',
	'material-1-form-3-content': u'ingredients',
	'material-1-form-3-is_answer': 'False',
	'material-2-type': 'Description',
	'material-2-subject': '4',
	'material-2-topic': '4',
	'material-2-privacy': '2',
	'material-2-title': u'fill the correct answer',
	'material-2-answer': u'in',
	'material-3-type': 'Choice',
	'material-3-subject': '4',
	'material-3-topic': '4',
	'material-3-privacy': '2',
	'material-3-title': u'choose the correct answer',
	'material-3-form-TOTAL_FORMS': '4',
	'material-3-form-INITIAL_FORMS': '0',
#	'material-3-form-MAX_NUM_FORMS': '10',
	'material-3-form-0-content': u'excluded',
	'material-3-form-0-is_answer': 'False',
	'material-3-form-1-content': u'to exclude',
	'material-3-form-1-is_answer': 'False',
	'material-3-form-2-content': u'exclusive of',
	'material-3-form-2-is_answer': 'True',
	'material-3-form-3-content': u'exclude',
	'material-3-form-3-is_answer': 'False',
	'material-4-type': 'Choice',
	'material-4-subject': '4',
	'material-4-topic': '4',
	'material-4-privacy': '2',
	'material-4-title': u'choose the correct answer',
	'material-4-form-TOTAL_FORMS': '4',
	'material-4-form-INITIAL_FORMS': '0',
#	'material-4-form-MAX_NUM_FORMS': '10',
	'material-4-form-0-content': u'what',
	'material-4-form-0-is_answer': 'False',
	'material-4-form-1-content': u'ones that',
	'material-4-form-1-is_answer': 'True',
	'material-4-form-2-content': u'which',
	'material-4-form-2-is_answer': 'False',
	'material-4-form-3-content': u'those',
	'material-4-form-3-is_answer': 'False',
}

MaterialGroup3_data = {
	'material_count': '2',
	'type': 'MaterialGroup',
	'subject': '4',
	'topic': '4',
	'privacy': '2',
	'title': u'英文語意群組題-The uncanny valley-2',
	'content': u"Most people are aware that it is very important to make sure that fruits are parts of your diet. Most fruits are full of vitamins A and C and are almost __1__ fat. However, there are a few fruits that are either insufficient in certain __2__ or are exaggerated too much in their benefits. First, almost all fruits are low __3__ calories, but apples and bananas are the ones that are at 100 calories or above. Second, you should never have put an avocado or olive on your fruit salad because of their high fat content. Third, blueberries and cranberries contain no vitamin A. Furthermore, most of the fruits are very good sources of vitamin C, __4__ grapes and apples which only have merely 5 percent. Last but not the least, almost half of all fruits contains less than 1 percent of the recommended daily allowance of calcium or iron. In conclusion, since fruits are necessary, make sure that you choose the right __5__ benefit you the best.",
}

count = 0
for key, value in Choice1_data.items():
	MaterialGroup3_data.update(
		{
			'material-{0}-{1}'.format(count, key): value,
		}
	)

count = count +1
for key, value in Choice1_data.items():
	MaterialGroup3_data.update(
		{
			'material-{0}-{1}'.format(count, key): value,
		}
	)

count = count +1
for key, value in Choice1_data.items():
	MaterialGroup3_data.update(
		{
			'material-{0}-{1}'.format(count, key): value,
		}
	)

count = count +1
for key, value in Choice1_data.items():
	MaterialGroup3_data.update(
		{
			'material-{0}-{1}'.format(count, key): value,
		}
	)

class basedSetup(TestCase):
	def setUp(self):
		super(basedSetup, self).setUp()
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

class basedSetupMaterial(basedSetup):
	def setUp(self):
		super(basedSetupMaterial, self).setUp()
		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Text1_data,
		)
		self.assertEqual(len(Text.objects.all()), previous_count + 1)

		previous_count = len(Text.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Text2_data,
		)
		self.assertEqual(len(Text.objects.all()), previous_count + 1)

#type:　TrueFalse

		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse1_data,
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)

		previous_count = len(TrueFalse.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			TrueFalse1_data,
		)
		self.assertEqual(len(TrueFalse.objects.all()), previous_count + 1)

#Type:　Choice

		previous_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_create'),
			Choice1_data,
		)
		self.assertEqual(len(Choice.objects.all()), previous_count + 1)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 4)

#Type = MaterialGroup

		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_creategroup'),
			MaterialGroup1_data
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

		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_choice_count = len(Choice.objects.all())
		previous_option_count = len(Option.objects.all())
		previous_description_count = len(Description.objects.all())
		previous_materialgroup_count = len(MaterialGroup.objects.all())
		previous_materialgroupdetail_count = len(MaterialGroupDetail.objects.all())
		response = self.client.post(
			reverse('MaterialADocument:material_creategroup'),
			MaterialGroup2_data,
		)
		self.assertEqual(len(MaterialGroup.objects.all()), previous_materialgroup_count + 1)
		self.assertEqual(len(Choice.objects.all()), previous_choice_count + 4)
		self.assertEqual(len(Option.objects.all()), previous_option_count + 16)
		self.assertEqual(len(Description.objects.all()), previous_description_count + 1)
		self.assertEqual(len(MaterialGroupDetail.objects.all()), previous_materialgroupdetail_count + 5)
		'''m = MaterialGroup.objects.first()
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, reverse('MaterialADocument:material_view', kwargs={
			'type': m.__class__.__name__,
			'id': m.id,
		}, ))'''

class basedSetupDocument(basedSetupMaterial):
	def setUp(self):
		super(basedSetupDocument, self).setUp()
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
				'material-0-seq': '0',
				'material-1-type': 'TrueFalse',
				'material-1-id': '2',
				'material-1-seq': '1',
			},
		)
		self.assertEqual(response.json()['status'], 'success')
		self.assertEqual(len(Document.objects.all()), previous_count + 1)
		self.assertEqual(len(TrueFalse.objects.all()), previous_TrueFalse_count + 2)

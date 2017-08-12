from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from .models import *

class loginViewTests(TestCase):

	@classmethod
	def setUpClass(cls):
		super(loginViewTests, cls).setUpClass()
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'root firstname', last_name = 'root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2017-01-01')
		root.set_password('root')
		root.auth_email = True
		root.auth_phone = True
		root.save()

	def test_correct_Text_case(self):	
		response = self.client.post(
			reverse('users:login'),
			{
				'username': 'root',
				'password': 'root',
			},
		)
		self.assertEqual(response.json()['status'], 'success')
		self.assertRedirects(response, '/')

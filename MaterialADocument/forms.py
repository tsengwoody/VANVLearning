# coding: utf-8
from django import forms
from django.forms import formset_factory
from .models import *
import json

EMPTY_OPTION = (('', u'---------'),)
TRUEFALSE_OPTION = ((True, u'是'), (False, u'否'),)
PRIVACY_OPTION = (
	(0, u'私人'),
	(1, u'特殊'),
	(2, u'公開'),
)

class MaterialBaseForm(forms.ModelForm):
	topic = forms.IntegerField(
		widget=forms.Select(
			choices = EMPTY_OPTION
		),
		label = u'主題',
	)

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(MaterialBaseForm, self).__init__(*args, **kwargs)
		choices = [('', u'---------')]
		choices = list(EMPTY_OPTION) + [(subject.id, subject.name) for subject in Subject.objects.all()]
		self.fields['subject'] = forms.IntegerField(
			widget=forms.Select(
				choices=choices
			),
			label=u'科目',
		)

	def clean(self):
		cleaned_data = super(MaterialBaseForm, self).clean()
		subject_id = cleaned_data.get("subject")
		topic_id = cleaned_data.get("topic")
		if subject_id and topic_id:
			SubjectToTopic = {}
			for subject in Subject.objects.all():
				SubjectToTopic[subject.id] = [topic.id for topic in subject.topic_set.all()]
			if topic_id not in SubjectToTopic[subject_id]:
				raise forms.ValidationError(
					"subject to topic not map",
					code="no_match",
				)

	def save(self, *args, **kwargs):
		commit = kwargs['commit']
		kwargs['commit'] = False
		instance = super(MaterialBaseForm, self).save(*args, **kwargs)
		instance.topic = Topic.objects.get(id=self.cleaned_data['topic'])
		if commit:
			instance.save()
		return instance

class SelectForm(forms.Form):
	type = forms.IntegerField(
		widget=forms.RadioSelect(
			choices = (
				(0, u'課文'),
				(1, u'是非題'),
				(2, u'選擇題'),
				(3, u'問答題'),
			)
		),
		label=u'類型',
	)

class MaterialGroupForm(MaterialBaseForm):
	class Meta:
		model = MaterialGroup
		fields = ['title', 'privacy', 'content']
		widgets = {
			'title': forms.TextInput(
				attrs={},
			),
			'privacy': forms.RadioSelect(
				attrs={},
				choices = PRIVACY_OPTION,
			),
			'content': forms.Textarea(
				attrs={},
			),
		}
		labels = {
			'title': u'標題',
			'privacy': u'權限',
			'content': u'內容',
		}
		help_texts = {
		}

	def __init__(self, *args, **kwargs):
		super(MaterialGroupForm, self).__init__(*args, **kwargs)
		new_order = ['subject', 'topic', 'privacy', 'title', 'content',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class TextForm(MaterialBaseForm):
	class Meta:
		model = Text
		fields = ['title', 'privacy', 'content']
		widgets = {
			'title': forms.TextInput(
				attrs={},
			),
			'privacy': forms.RadioSelect(
				attrs={},
				choices = PRIVACY_OPTION,
			),
			'content': forms.Textarea(
				attrs={},
			),
		}
		labels = {
			'title': u'標題',
			'privacy': u'權限',
			'content': u'內容',
		}
		help_texts = {
		}

	def __init__(self, *args, **kwargs):
		super(TextForm, self).__init__(*args, **kwargs)
		new_order = ['subject', 'topic', 'privacy', 'title', 'content',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class TrueFalseForm(MaterialBaseForm):
	class Meta:
		model = TrueFalse
		fields = ['title', 'privacy', 'answer']
		widgets = {
			'title': forms.Textarea(
				attrs={},
			),
			'privacy': forms.RadioSelect(
				attrs={},
				choices = PRIVACY_OPTION,
			),
			'answer': forms.RadioSelect(
				attrs={},
				choices = TRUEFALSE_OPTION,
			),
		}
		labels = {
			'title': u'題目',
			'privacy': u'權限',
			'answer': u'解答',
		}
		help_texts = {
		}

	def __init__(self, *args, **kwargs):
		super(TrueFalseForm, self).__init__(*args, **kwargs)
		new_order = ['subject', 'topic', 'privacy', 'title', 'answer',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class ChoiceForm(MaterialBaseForm):
	class Meta:
		model = Choice
		fields = ['title', 'privacy',]
		widgets = {
			'title': forms.Textarea(
				attrs={},
			),
			'privacy': forms.RadioSelect(
				attrs={},
				choices = PRIVACY_OPTION,
			),
		}
		labels = {
			'title': u'題目',
			'privacy': u'權限',
		}
		help_texts = {
		}

	def __init__(self, *args, **kwargs):
		super(ChoiceForm, self).__init__(*args, **kwargs)
		new_order = ['subject', 'topic', 'privacy', 'title',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class OptionForm(forms.ModelForm):
	class Meta:
		model = Option
		fields = ['content', 'is_answer',]
		widgets = {
			'content': forms.Textarea(
				attrs={},
			),
			'is_answer': forms.RadioSelect(
				attrs={},
				choices = TRUEFALSE_OPTION,
			),
		}
		labels = {
			'content': u'選項',
			'is_answer': u'解答',
		}

	def save(self, *args, **kwargs):
		commit = kwargs['commit']
		kwargs['commit'] = False
		choice = kwargs.pop('choice', None)
		instance = super(OptionForm, self).save(*args, **kwargs)
		instance.choice = choice
		if commit:
			instance.save()
		return instance

class DescriptionForm(MaterialBaseForm):
	class Meta:
		model = Description
		fields = ['title', 'privacy', 'answer']
		widgets = {
			'title': forms.Textarea(
				attrs={},
			),
			'privacy': forms.RadioSelect(
				attrs={},
				choices = PRIVACY_OPTION,
			),
			'answer': forms.Textarea(
				attrs={},
			),
		}
		labels = {
			'title': u'題目',
			'privacy': u'權限',
			'answer': u'解答',
		}
		help_texts = {
		}

	def __init__(self, *args, **kwargs):
		super(DescriptionForm, self).__init__(*args, **kwargs)
		new_order = ['subject', 'topic', 'privacy', 'title', 'answer',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class MaterialForm(object):
	def __init__(self):
		self.material = []

	def fill(self, data, origin_material, user,):
		if data['type'] in ['Text', 'TrueFalse', 'Choice', 'Description', 'MaterialGroup', ]:
			exec("form = {}Form(data)".format(data['type']))
		else:
			raise TypeError('type not valid')
		if not form.is_valid():
			raise ValueError(json.dumps(form.errors))
		material = form.save(commit=False)
		material.origin_material = origin_material
		material.create_user = user
		material.save()
		self.material.append(material)
		if data['type'] == 'Choice':
			OptionFormSet = formset_factory(OptionForm)
			formSet = OptionFormSet(data)
			if not formSet.is_valid():
				raise ValueError(json.dumps(formSet.errors))
			self.material = self.material + [form.save(choice=material, commit=True) for form in formSet]
		return self.material

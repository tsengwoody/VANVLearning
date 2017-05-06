# coding: utf-8
from django import forms
from .models import *

EMPTY_OPTION = (('', u'---------'),)
TRUEFALSE_OPTION = ((True, u'是'), (False, u'否'),)
PRIVACY_OPTION = (
	(0, u'私人'),
	(1, u'特殊'),
	(2, u'公開'),
)

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

	class Media:
		css = {
		}
		js = ('/static/SelectForm.js',)

class TextForm(forms.ModelForm):
	topic = forms.IntegerField(
		widget=forms.Select(
			choices = EMPTY_OPTION
		),
		label = u'主題',
	)

	class Meta:
		model = Text
		fields = ['title', 'privacy', 'content']
		widgets = {
			'title': forms.Textarea(
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
	class Media:
		css = {
		}
		js = ('/static/TextForm.js',)

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(TextForm, self).__init__(*args, **kwargs)
		choices = [('', u'---------')]
		choices = list(EMPTY_OPTION) + [(subject.id, subject.name) for subject in Subject.objects.all()]
		self.fields['subject'] = forms.IntegerField(
			widget=forms.Select(
				choices=choices
			),
			label=u'科目',
		)
		new_order = ['subject', 'topic', 'privacy', 'title', 'content',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class TrueFalseForm(forms.ModelForm):
	topic = forms.IntegerField(
		widget=forms.Select(
			choices = EMPTY_OPTION
		),
		label = u'主題',
	)

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
	class Media:
		css = {
		}
		js = ('/static/TrueFalseForm.js',)

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(TrueFalseForm, self).__init__(*args, **kwargs)
		choices = [('', u'---------')]
		choices = list(EMPTY_OPTION) + [(subject.id, subject.name) for subject in Subject.objects.all()]
		self.fields['subject'] = forms.IntegerField(
			widget=forms.Select(
				choices=choices
			),
			label=u'科目',
		)
		new_order = ['subject', 'topic', 'privacy', 'title', 'answer',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

class ChoiceForm(forms.ModelForm):
	topic = forms.IntegerField(
		widget=forms.Select(
			choices = EMPTY_OPTION
		),
		label = u'主題',
	)

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
	class Media:
		css = {
		}
		js = ('/static/ChoiceForm.js',)

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(ChoiceForm, self).__init__(*args, **kwargs)
		choices = list(EMPTY_OPTION) + [(subject.id, subject.name) for subject in Subject.objects.all()]
		self.fields['subject'] = forms.IntegerField(
			widget=forms.Select(
				choices=choices
			),
			label=u'科目',
		)
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

class DescriptionForm(forms.ModelForm):
	topic = forms.IntegerField(
		widget=forms.Select(
			choices = EMPTY_OPTION
		),
		label = u'主題',
	)

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
	class Media:
		css = {
		}
		js = ('/static/DescriptionForm.js',)

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(DescriptionForm, self).__init__(*args, **kwargs)
		choices = [('', u'---------')]
		choices = list(EMPTY_OPTION) + [(subject.id, subject.name) for subject in Subject.objects.all()]
		self.fields['subject'] = forms.IntegerField(
			widget=forms.Select(
				choices=choices
			),
			label=u'科目',
		)
		new_order = ['subject', 'topic', 'privacy', 'title', 'answer',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in new_order)

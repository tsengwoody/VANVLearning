﻿# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from users.models import User

import json

class Subject(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Topic(models.Model):
	subject = models.ForeignKey(Subject)
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.subject.name +':' +self.name

class Material(models.Model):
	topic = models.ForeignKey(Topic)
	title = models.TextField(blank=True, null=True) #值為空表示為群組題，例如：克漏字
	privacy = models.IntegerField()
	PRIVACY = {'PRIVATE':0, 'VIP':1, 'PUBLIC':2}
	origin_material = models.BooleanField()
	create_time = models.DateTimeField(default = timezone.now)
	create_user = models.ForeignKey(User)
	update_time = models.DateTimeField(blank=True, null=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.topic.name +str(self.id)

	def serialized(self):
		serialize = {}
		for field in self._meta.fields:
			value = getattr(self, field.name)
			if isinstance(value, models.Model):
				value = {'name': unicode(value), 'href': ''}
			else:
				try:
					json.dumps(value)
				except:
					value = unicode(value)
			serialize.update({field.name: value})
		return serialize

	def serialized_abstract(self):
		serialize = {}
		for field in ['topic', 'title', 'create_time', 'create_user']:
			value = getattr(self, field)
			if isinstance(value, models.Model):
				value = {'name': unicode(value), 'href': ''}
			else:
				try:
					json.dumps(value)
				except:
					value = unicode(value)
			serialize.update({field: value})
		return serialize

class Text(Material):
	title = models.CharField(max_length=100)
	content = models.TextField()
	from_material = models.ForeignKey('Text', blank=True, null=True)

class TrueFalse(Material):
	answer = models.BooleanField()
	from_material = models.ForeignKey('TrueFalse', blank=True, null=True)

class Choice(Material):
	from_material = models.ForeignKey('Choice', blank=True, null=True)

class Option(models.Model):
	choice = models.ForeignKey(Choice)
	content = models.TextField()
	is_answer = models.BooleanField()

	def __unicode__(self):
		return str(self.choice.id) +'-' +str(self.id)

class Description(Material):
	answer = models.TextField()
	from_material = models.ForeignKey('Description', blank=True, null=True)

class MaterialGroup(Material):
	title = models.CharField(max_length=100)
	content = models.TextField()
	from_material = models.ForeignKey('MaterialGroup', blank=True, null=True)

	def delete(self, *args, **kwargs):
		for i in self.materialgroupdetail_set.all():
			i.delete()
		super(MaterialGroup, self).delete(*args, **kwargs)

	def __unicode__(self):
		return str(self.__class__) +'-' +str(self.id)

class MaterialGroupDetail(models.Model):
	material_group = models.ForeignKey(MaterialGroup, on_delete=models.SET_NULL, blank=True, null=True)
#	material_group = models.ForeignKey(MaterialGroup, on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	material = GenericForeignKey('content_type', 'object_id')
	seq = models.PositiveIntegerField()

	def __unicode__(self):
		return str(self.material_group.id) +'-' +str(self.seq)

	def clean(self):
		ValidationError_dict = {}
		if self.material_group.topic != self.material.topic:
			ValidationError_dict.update({
				'topic': ValidationError(_('material not match materialgroup privacy'), code='not_match'),
			})
		if self.material_group.privacy != self.material.privacy:
			ValidationError_dict.update({
				'topic': ValidationError(_('material not match materialgroup topic'), code='not_match'),
			})
		if ValidationError_dict != {}:
			raise ValidationError(ValidationError_dict)

	def delete(self, *args, **kwargs):
		self.material.delete()
		super(MaterialGroupDetail, self).delete(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.full_clean()
		super(MaterialGroupDetail, self).save(*args, **kwargs)

class ContentPiece(models.Model):
	content = models.TextField()

class Image(models.Model):
	short_description = models.CharField(max_length=100)
	long_description = models.TextField(blank=True, null=True)
	image = models.FileField(upload_to='image/')

class Document(models.Model):
	type = models.IntegerField()
	TYPE = {'CONTENT':0, 'exam': 1}
	subject = models.ForeignKey(Subject)
	topic = models.ManyToManyField(Topic)
	title = models.TextField()
	privacy = models.IntegerField()
	PRIVACY = {'PRIVATE':0, 'VIP':1, 'PUBLIC':2}
	abstract = models.TextField(blank=True, null=True)
	parent_document = models.ForeignKey('Document')
	create_time = models.DateTimeField(default = timezone.now)
	create_user = models.ForeignKey(User)
	update_time = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return self.tilte

class DocumentDetail(models.Model):
	document = models.ForeignKey(Document)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	material = GenericForeignKey('content_type', 'object_id')
	seq = models.PositiveIntegerField()
	score = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return str(self.document.id) +'-' +str(self.seq)

class Learn(models.Model):
	document = models.ForeignKey(Document)
	create_time = models.DateTimeField(default = timezone.now)
	create_user = models.ForeignKey(User)
	update_time = models.DateTimeField(blank=True, null=True)

class Exam(models.Model):
	document = models.ForeignKey(Document)
	score = models.IntegerField(blank=True, null=True)
	duration = models.IntegerField(blank=True, null=True)
	create_time = models.DateTimeField(default = timezone.now)
	create_user = models.ForeignKey(User)
	update_time = models.DateTimeField(blank=True, null=True)

class Answer(models.Model):
	exam = models.ForeignKey(Exam)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	material = GenericForeignKey('content_type', 'object_id')
	answer_content = models.TextField()
	create_time = models.DateTimeField(default = timezone.now)
	create_user = models.ForeignKey(User)

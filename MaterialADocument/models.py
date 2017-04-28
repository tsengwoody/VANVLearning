# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from users.models import User

class Subject(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Topic(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Material(models.Model):
	subject = models.ForeignKey(Subject)
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
		return self.subject.name +str(self.id)

class Text(Material):
	title = models.CharField(max_length=100)
	content = models.TextField()
	from_material = models.ForeignKey('Text')

class TrueFalse(Material):
	answer = models.BooleanField()
	from_material = models.ForeignKey('TrueFalse')

class Choice(Material):
	from_material = models.ForeignKey('Choice')

class Option(models.Model):
	choice = models.ForeignKey(Choice)
	content = models.TextField()
	is_answer = models.BooleanField()

	def __unicode__(self):
		return str(self.choice.id) +'-' +str(self.id)

class Description(Material):
	answer = models.TextField()
	from_material = models.ForeignKey('Description')

class MaterialGroup(Material):
	title = models.CharField(max_length=100)
	content = models.TextField()
	from_material = models.ForeignKey('MaterialGroup')
	material_count = models.IntegerField()

class MaterialGroupDetail(models.Model):
	material_group = models.ForeignKey(MaterialGroup)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	material = GenericForeignKey('content_type', 'object_id')
	seq = models.PositiveIntegerField()

	def __unicode__(self):
		return str(self.material_group.id) +'-' +str(self.seq)

class ContentPiece(models.Model):
	content = models.TextField()

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
	update_time = models.DateTimeField(blank=True, null=True)

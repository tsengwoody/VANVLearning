# coding=utf-8
from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Text)
admin.site.register(TrueFalse)
admin.site.register(Choice)
admin.site.register(Option)
admin.site.register(Description)
admin.site.register(MaterialGroup)
admin.site.register(MaterialGroupDetail)
admin.site.register(ContentPiece)
admin.site.register(Document)
admin.site.register(DocumentDetail)
admin.site.register(Learn)
admin.site.register(Exam)
admin.site.register(Answer)

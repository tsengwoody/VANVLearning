# coding=utf-8
from django.shortcuts import render

# Create your views here.

from .forms import *
from .models import *

def material_create(request, template_name='MaterialADocument/material_create.html'):
	selectForm = SelectForm()
	textForm = TextForm()
	tfForm = TrueFalseForm()
	choiceForm = ChoiceForm()
	optionForm = OptionForm()
	descriptionForm = DescriptionForm()
	return render(request, template_name, locals())

def material_creategroup(request, template_name='MaterialADocument/material_creategroup.html'):
	return render(request, template_name, locals())
from django.shortcuts import render
from django.http import HttpResponse
from .models import Category,Company,Section

def home(request):
    category = Category.objects.all()
    company = Company.objects.all()
    section = Section.objects.all()
    return render(request, 'shop/test.html', {'category': category, 'company': company, 'section': section})
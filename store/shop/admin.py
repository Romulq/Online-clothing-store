from django.contrib import admin
from .models import Section, Category, Company, Product

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'section')
    search_fields = ['name', 'section__name']

admin.site.register(Section)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Company)
admin.site.register(Product)

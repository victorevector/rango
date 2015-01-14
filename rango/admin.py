from django.contrib import admin
from rango.models import Category, Page

admin.site.register(Category)

class PageAdmin(admin.ModelAdmin):
	# sets up the following fields as columns in rango/pages
	list_display = ['title', 'category','url']
	# Allows you to display fields within Fieldsets when you select a specific page
	# And allows you to change vertical ordering of the following fields
	# fieldsets = [
	# 	(None,		 {'fields': ['title']}),
	# 	('Category', {'fields': ['category']}),
	# 	('URL',		 {'fields': ['url']}),
	# 	('Views',	 {'fields': ['views']}),
	# ]
	fieldsets = [
		(None, {'fields': ['title',
						   'category',
						   'url',
						   'views']}),
	]

admin.site.register(Page, PageAdmin)
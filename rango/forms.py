from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(),required=False)
	#An inline class to provide additional information on the form.
	class Meta:
		#provide an association between the ModelForm and a model
		model=Category
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	class Meta:
		#provides an association between the ModelForm and a model
		model = Page
			#what Fields do we want to include in our form?
	#this way we dont need every field in the model present.
	#some fields may not allow NULL values, so we may not want to include them...
	#Here we are hiding the foreign key.
	#we can either exclude the category field from the form,
		exclude = ('category',)
	#or specify the fields to include(i.e. not include the category field)
	#fields = ('title','url','views')
	def clean(self):
		#self.cleaned_data conjures up all the form information recorded in the instantiation of the Page model object. 
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		#if url is not empty and doesn't start with 'http://',prepend 'http://'
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

			return cleaned_data



from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm

def index(request):
	#Query the database for a list of ALL categories currently stored
	#Order the categories by no. likes in descending order
	#Retrieve the top 5 only- or all if less than 5
	#Place the list in our context_dict dictionary which will be passed to the template engine
	category_list = Category.objects.order_by('-likes')[:5] #'-' responsible for descending order
	categories_mostviewed = Category.objects.order_by('-views')[:5]
	context_dict = {
		'categories_mostliked': category_list,
		'categories_mostviewed': categories_mostviewed,
		}

	# Return a rendered response to send to the client
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render(request, 'rango/index.html', context_dict)

	# return HttpResponse("Rango says: Hello world! <br/> <a href='/rango/about'>About</a>")

def about(request):
	context_dict = {'name': "Johnny Depp"}
	return render(request, 'rango/about.html', context_dict)

	# return HttpResponse("Rango says here is the about page. </br> <a href ='/rango/'> Index </a>")

def category(request, category_name_slug):
	#create a context dictionary which we can pass to the templated rendering engine.
	context_dict = {}

	try:
		#can we find a category name slug with the given name?
		#if we can't, the .get() method raises a DoesNotExist exception
		#so the .get()method returns one model instance or raises an exception
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		#eg. context_dict['category_name'] = 'Python' => {'category_name': 'Python'}

		#retrieve all of the pages associated with the category retrieved above
		#note that filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category)

		#adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		#we also add the category object from the db to the context dictionary
		#we'll use this in the template to verify that the category exists
		context_dict['category'] = category

		# By the end, context_dict will be populated as such...
		# context_dict = {
		# 'category_name': category.name,
		# 'pages': [Page.objects.filter(category=category),],
		# 'category': Category.objects.get(slug=category_name_slug),
		# } 
	except Category.DoesNotExist:
		#We get here if we didn't find the specified category.
		#don't do anything-- the template displays the 'no category' message for us.
		pass
		context_dict = {'category':category_name_slug}
		return render(request,'rango/error.html',context_dict)


	#go render the response and return it to the client.
	return render(request,'rango/category.html',context_dict)

def add_category(request):
	#a http post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#have we been provided with a valid form?
		if form.is_valid():
			#save the new category to the database
			form.save(commit=True)

			#now call the index() view.
			#the user will be shown the homepage
			return index(request)
		else:
			#the supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		#if the request was not a POST, display the form to enter details.
		form = CategoryForm()

	#bad form (or form details), no form supplied...
	#render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form':form})

from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime

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

	#get the number of visits to the site.
	# we use the COOKIES.get() function to obtain the visits cookies 
	# if the cookies exists, the value returned is casted to an integer
	# if the cookie doesnt exist we default to zero and cast that
	visits = int(request.COOKIES.get('visits', '1')) #get(keyword, default value if value not found)
	
	reset_last_visit_time = False
	response = render(request, 'rango/index.html', context_dict)
	#Does the cookie last_visit exist?
	if 'last_visit' in request.COOKIES:
		#Yes it does! get the cookie's value.
		last_visit = request.COOKIES['last_visit']
		#cast the value to a python date/time object
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		#if it's been more than a day since the last visit...
		if (datetime.now()-last_visit_time).days > 0:
			visits = visits + 1
			#... flag that the cookie last visit needs to be updated.
			reset_last_visit_time = True
	else:
		#cookies last_visit doesnt exist, so flag that it should be set.
		reset_last_visit_time = True

		context_dict['visits'] = visits

		#obtain our response object early so we can add cookie information
		response = render(request, 'rango/index.html', context_dict)

	if reset_last_visit_time:
		response.set_cookie('last_visit', datetime.now())
		response.set_cookie('visits',visits)

	#return response back to the user, updating any cookies that need changed.
	return response

	# Return a rendered response to send to the client
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	# return render(request, 'rango/index.html', context_dict)

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
		context_dict['category_name_slug']=category_name_slug
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
		context_dict = {'category':category_name_slug, 'category_name_slug':category_name_slug}
		return render(request,'rango/error.html',context_dict)


	#go render the response and return it to the client.
	return render(request,'rango/category.html',context_dict)

@login_required
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

@login_required
def add_page(request,category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat=None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page=form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				#call views.category == will render the relevant category page
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
	context_dict = {'form': form, 'category': cat}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	#a boolean value for telling the template whether the registration was successful.
	#set to False initially. Code changes value to True when registration succeeds.
	registered = False

	#if it's a HTTP POST, we're intersted in processing form data. 
	if request.method == 'POST':
		#attempt to grab information from the raw form information
		#note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#if the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			#save the user's form data to the database
			user=user_form.save()

			#Now we hash the password with the set_password method.
			#once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			#now sort out the UserProfile instance
			#since we need to set the user attribute ourselves we set commit=False
			profile = profile_form.save(commit=False)
			profile.user = user

			#did the user provide a profile picture?
			#if so, we need to get it from the input form and put it in the UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			#now we save the UserProfile model instance.
			profile.save()

			#update our variable to tell the template registration was successful.
			registered = True

		#invalid form or forms - mistakes or something else?
		#print problems to the terminal
		#they'll also be shown to the user
		else:
			print user_form.errors, profile_form.errors

		#not a HTTP post, so we render our form using two ModelForm instances
		#these forms will be blank, ready for user input
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	#render the template depending on the context
	return render(request,
		'rango/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	#if the request is a HTTP post, try to pull out the relevant information
	if request.method == 'POST':
		#gather the username and password provided by the user
		#this information is obtained from the login form
		username = request.POST['username']
		password = request.POST['password']

		#use django's machinery to attempt to see if the username/password
		#combination is valid- a User object is returned if it is.
		user = authenticate(username=username, password=password)

		#if we have a User object, the details are correct
		#if None(python's way of representing the absence of a value), no user
		#with matching credentials was found.
		if user:
			#is the account active? it could have been disabled?
			if user.is_active:
				#if the account is valid and active, we can log the user in
				#we'll send the user back to the homepage
				login(request,user)
				return HttpResponseRedirect('/rango/')
			else:
				#an inactive account was used-- no logging in!
				return HttpResponse("Your Rango account is disabled")
		else:
			#bad login details were provided. so we cant log the user in
			print 'Invalid login details: {0}, {1}'.format(username, password)
			return HttpResponse('Invalid login details supplied')

		#the request is not an HTTP POST, so display the login form
		#this scenario would most likely be a HTTP GET

	else:
		#No context variables to pass to the template system, hence the blank dictionary object...
		return render(request, 'rango/login.html',{})

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
	#since we know the user is logged in, we can now just log them out.
	logout(request)

	#take the user back to the homepage
	return HttpResponseRedirect('/rango/')

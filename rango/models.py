from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category,self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length = 128)
	url = models.URLField()
	views = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.title
		
class UserProfile(models.Model):
	#this line is required. it links UserProfile to a User model instance.
	#this way, UserProfile can be 'attached' to the User object
	#in other words, a UserProfile that has a user
	# just like how your facebook or gmail user profile is separate from the user account itself
	user = models.OneToOneField(User)

	#the additional attributes we wish to include. Fields can be left blank
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	#override the __unicode__()method to return out something meaningful!
	def __unicode__(self):
		return self.user.username
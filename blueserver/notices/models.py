from django.db import models

# Create your models here.
class Notice(models.Model):
	title = models.CharField(max_length=200)

	tags = models.CharField(max_length=200)
	author = models.CharField(max_length=100)
	body = models.TextField()
	pub_date = models.DateTimeField('date published')
	del_date = models.DateTimeField('delete by date')

	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	name = models.CharField(max_length=100)
	userKey = models.CharField(max_length=10)

	def __unicode__(self):
		return self.name
from django.db import models
from django.conf import settings

class Env_Rooms(models.Model):
	"""
	Contains the list of Environments
	"""
	env_name = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.env_name

class Upload(models.Model):
	"""
	Contains the path to uploaded images
	"""
	name = models.CharField(max_length=255)
	upload = models.FileField(upload_to=settings.FILE_UPLOAD_PATH)
	
	def __unicode__(self):
		return self.name

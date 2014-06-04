from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from env_rooms.models import Env_Rooms,Upload
from django.template import RequestContext
from django.conf import settings
import logging
import redis
import tornado.escape
from forms import UploaderForm
import json

def redis_connect():
        REDIS_HOST = settings.REDIS_HOST
        REDIS_PORT = settings.REDIS_PORT
        REDIS_PWD = settings.REDIS_PWD
        REDIS_USER = settings.REDIS_USER
        client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))
        return client

def envs_home(request):
	envs = Env_Rooms.objects.all()
	return render_to_response('env_rooms/env_room_index.html', {'envs':envs, 'STATIC_SERVER_URL':settings.STATIC_SERVER_URL} )

def env(request,env):
	logging.info('Connecting to Redis and fetching last 50 messages')
	client = redis_connect()
	last_50_messages = client.lrange(env,-50, -1)	
	messages = []
	for message in last_50_messages:
		messages.append(tornado.escape.json_decode(message)["html"])
	return render_to_response('env_rooms/room.html',{'env':env, 'STATIC_SERVER_URL':settings.STATIC_SERVER_URL, 'MEDIA_URL':settings.MEDIA_URL, 'messages':messages},
				context_instance=RequestContext(request))

def upload(request):
	logging.info('Inside upload view')
	response_data = {}
	if request.is_ajax():
		logging.info('Is_AJAX() returned True')	
		form = UploaderForm(request.POST, request.FILES)
		  
		if form.is_valid():
			logging.info('Uploaded Data Validated')
			upload = Upload( upload=request.FILES['upload'] )
			upload.name = request.FILES['upload'].name
			upload.save()
			logging.info('Uploaded Data Saved in Database and link is %s' % upload.upload)			

			response_data['status'] = "success"
			response_data['result'] = "Your file has been uploaded !!"
			response_data['body'] = "/%s" % upload.upload
			
			return HttpResponse(json.dumps(response_data), content_type="application/json")

	response_data['status'] = "error"
	response_data['result'] = "Something went wrong.Try Again !!"

	return HttpResponse(json.dumps(response_data), content_type='application/json')	

#!/optusr1/aimsys/tools/gauravy/local/bin/python

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from django.conf import settings
import brukva
import logging
from threading import Timer
import uuid
import os.path

tornado.options.define('port', type=int, default=8080)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
        	user = self.get_cookie("chatdemo_user")
        	if not user: return None
        	return user

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self, env):
		logging.info('New connection opened for env %s', env)
		self.client = redis_connect()
		self.room = env
		self.client.subscribe(env)
		self.subscribed = True
		self.client.listen(self.on_messages_published)
		logging.info('New user connected to %s chat room', env)		
	
	def on_messages_published(self, message):
		m = tornado.escape.json_decode(message.body)
		logging.info('from function on_messages_published')
		logging.info('Sending back data on_messages_published')
		self.write_message(m)

	def on_message(self, data):
		logging.info('Received new message %r', data)
		datadecoded = tornado.escape.json_decode(data)
		message = {
		"id": str(uuid.uuid4()),
            	"body": datadecoded["body"],
		}
		logging.info(datadecoded["body"])

		if (datadecoded["message_type"] == "text"):
			message["html"] = tornado.escape.to_basestring(self.render_string("message.html", input_to_template=message))
		else:
			message["html"] = tornado.escape.to_basestring(self.render_string("message_img.html", input_to_template=message))

		logging.info('Data decoded, now publish in Redis in %s channel', self.room)
		message_encoded = tornado.escape.json_encode(message)
		self.application.client.rpush(self.room, message_encoded)
		self.application.client.publish(self.room, message_encoded)
		return

	def on_close(self):
		logging.info("socket closed, cleaning up resources now")
		if hasattr(self, 'client'):
			if self.subscribed:
				self.client.unsubscribe(self.room)
				self.subscribed = False
			t = Timer(0.1, self.client.disconnect)
			t.start()	

def redis_connect():
	REDIS_HOST = settings.REDIS_HOST
	REDIS_PORT = settings.REDIS_PORT 
	REDIS_PWD = settings.REDIS_PWD
	REDIS_USER = settings.REDIS_USER
	client = brukva.Client(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PWD)
	client.connect()
	return client	

class Application(tornado.web.Application):
	def __init__(self):
		wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
		handlers = [
			(r"/chatsocket/(?P<env>[\w@]+)", ChatSocketHandler),
        		('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        	]
		
		settings = dict(
			cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
			template_path=os.path.join(os.path.dirname(__file__), "tornado_templates"),
			login_url="/login",
			xsrf_cookies= False,
			autoescape="xhtml_escape",
			db_name = 'chat',
			)	
		tornado.web.Application.__init__(self, handlers, **settings)
		self.usernames = {}
		self.client = redis_connect()
	
def main():
	tornado.options.parse_command_line()
	application = Application()
	application.listen(tornado.options.options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()

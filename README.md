MultipleChatRoom-Using-Torndo-Django-and-Redis
==============================================

Mutiple Chat Room using Tornado,Django and Redis. 
Tornado is used for running Django and handle Websocket requests so that all the chat rooms can transfer data real-time.
Chat Rooms can be added from Django Admin Panel.
Redis Pub/Sub Feature is used for each chat room.

Main URLs
=========

http://<server>:<port>/envs --> Lists down all the Chat Rooms available . 
                                Chat Rooms are stored in the database in the table "Env_Rooms" ( can be found in models.py of env_rooms app).




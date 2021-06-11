from django.test import TestCase

from rest_framework.test import APITestCase

from .models import EventMain
from .serializers import EventMainSerializer
from user.models import CustomUser

import json


class TestMainEvent(APITestCase):

	def setUp(self):
		self.url = "/event-main/event/"
		CustomUser.objects._create_user(email="phong@gmail.com"
			, password="123456")
				

	def test_post_mainevent_success(self):
		user = CustomUser.objects.get(email="phong@gmail.com")
		url = "/event-main/event/"

		data = {
		    "address": "any random address",
		    "city": "cityB",
		    "state": "stateB",
		    "country": "countryB",
		    "author_id": int(user.id),
		    "title": "Hackaton",
		    "description": "I don't know how to spell well",
		    "date": "2020-07-03",
		    "time": "12:30",
		    "max_seat": 3,
		    "features": [
		        {"feature_name": "Programming"}
		    ]
		}
		res = self.client.post(self.url, data=data, format='json')
		self.assertEqual(res.status_code, 201)

	def test_put_mainevent_success(self):

		user = CustomUser.objects.get(email="phong@gmail.com")
		

		# create event main
		data = {
		    "address": "any random address",
		    "city": "cityB",
		    "state": "stateB",
		    "country": "countryB",
		    "author_id": int(user.id),
		    "title": "Hackaton",
		    "description": "I don't know how to spell well",
		    "date": "2020-07-03",
		    "time": "12:30",
		    "max_seat": 3,
		    "features": [
		        {"feature_name": "Programming"}
		    ]
		}
		res = self.client.post(self.url, data=data, format='json')
		self.assertEqual(res.status_code, 201)

		# get event main list
		res1 = self.client.get(self.url)
		self.assertEqual(res1.status_code, 200)
		event_main = res1.json()[0]

		# update event main
		event_main["max_seat"] = 5
		print(str(event_main["id"]))
		res2 = self.client.put(self.url + str(event_main["id"]), data=json.dumps(event_main), content_type='application/json')
		self.assertEqual(res2.status_code, 200)

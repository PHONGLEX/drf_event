from celery.decorators import task
from celery import shared_task
import time
import requests


@task()
def test():
	time.sleep(5)
	print("Hello Async")


@task()	
def populate_cat():
	url = "https://api.thecatapi.com/v1/images/search"

	try:
		res = requests.get(url)
	except requests.ConnectionError as e:
		raise Exception("Failed operation", e)

	if res.status_code in [200,201]:
		# create cat entry
		data = res.json()[0]
		image_url = data.get("url", "")
		from event_controller.models import Cat
		Cat.objects.create(url=image_url)
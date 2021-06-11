from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from user.serializers import AddressGlobalSerializer
from .serializers import (EventMainSerializer, EventFeatureSerializer, EventAttenderSerializer)
from .models import EventMain, EventFeature, EventAttender
from user.models import AddressGlobal


class EventMainView(ModelViewSet):
	serializer_class = EventMainSerializer
	queryset = EventMain.objects.select_related("author", "address_info").prefetch_related("event_features")

	def create(self, request, *args, **kwargs):
		a_serializer = AddressGlobalSerializer(data=request.data)
		a_serializer.is_valid(raise_exception=True)
		a_serializer.save()

		data = {**request.data, "address_info_id": a_serializer.data['id']}

		e_serializer = self.serializer_class(data=data)
		if not e_serializer.is_valid():
			AddressGlobal.objects.filter(id=a_serializer.data["id"]).delete()
			raise Exception(e_serializer.errors)
		e_serializer.save()

		features = request.data.get("features", None)		
		if not features:
			AddressGlobal.objects.filter(id=a_serializer.data['id']).delete()
			raise Exception("features field is required")

		if not isinstance(features, list):
			features = [features]

		data = []
		for f in features:
			if not isinstance(f, dict):
				AddressGlobal.objects.filter(id=a_serializer.data['id']).delete()
				raise Exception("Feature instance must be an object")
			data.append({
				**f, "eventmain_id": e_serializer.data["id"]
				})
		
		f_serializer = EventFeatureSerializer(data=data, many=True)
		if not f_serializer.is_valid():
			AddressGlobal.objects.filter(id=a_serializer.data["id"]).delete()
			raise Exception(f_serializer.errors)

		f_serializer.save()

		return Response((self.serializer_class(self.get_queryset().get(id=e_serializer.data["id"]))).data, status="201")

	def update(self, request, *arg, **kwargs):
		# get current instance
		instance = self.get_object()
		evt_serializer = self.serializer_class(data=request.data
			, instance=instance, partial=True)
		evt_serializer.is_valid(raise_exception=True)
		evt_serializer.save()

		add_serializer = AddressGlobalSerializer(data=request.data
			, instance=instance.address_info, partial=True)		
		add_serializer.is_valid(raise_exception=True)
		add_serializer.save()

		features = request.data.get("features", None)
		if features:
			if not isinstance(features, list):
				features = [features]

			data = []
			for f in features:
				if not isinstance(f, dict):
					raise Exception("Feature instance must be an object")
				data.append({
					**f,
					"eventmain_id": evt_serializer.data["id"]
					})

			f_serializer = EventFeatureSerializer(data=data, many=True)
			f_serializer.is_valid(raise_exception=True)
			f_serializer.save()
		return Response(self.serializer_class(self.get_object()).data, status=200)


class EventAttenderView(ModelViewSet):
	serializer_class = EventAttenderSerializer
	queryset = EventAttender.objects.select_related("user", "eventmain")

	def create(self, request, *args, **kwargs):
		# we need to validate so don't save the data at this time
		at_serializer = self.serializer_class(data=request.data)
		at_serializer.is_valid(raise_exception=True)
		
		evt = EventMainView.queryset.filter(id=at_serializer.validated_data["eventmain_id"])

		if not evt:
			raise Exception("Event does not exist")

		evt = evt[0]

		# check if user already exist
		is_user_reg = self.queryset.filter(eventmain_id=evt.id
			, user_id=at_serializer.validated_data["user_id"])
		if is_user_reg:
			raise Exception("you already registered for event")

		# check if the maximum seat has not reached
		at_count = self.queryset.filter(eventmain_id=evt.id).count()

		if not at_count < evt.max_seat:
			raise Exception("Maximum attenders taken")

		# check time
		at_time = at_serializer.validated_data["time"]
		if at_time < evt.time:
			raise Exception("You are too early")

		at_serializer.save()
		return Response(at_serializer.data, status=201)

from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer


from rest_framework.viewsets import ModelViewSet


class CustomUserView(ModelViewSet):
	serializer_class = CustomUserSerializer
	queryset = CustomUser.objects.prefetch_related("user_profile", "user_profile__address")


class UserProfileView(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.select_related("user", "address_info")
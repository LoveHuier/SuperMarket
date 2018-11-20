from rest_framework import viewsets
from rest_framework import mixins

from .models import UserFav
from .serializers import UserFavSerializer


# Create your views here.

class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

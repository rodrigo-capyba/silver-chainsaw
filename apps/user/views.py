from rest_framework.viewsets import ModelViewSet

from django.utils.translation import gettext_lazy as _

from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

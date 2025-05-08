from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from users.models import CustomUser
from users.serializer import UserCreateSerializer, UserSerializer
from config.permissions import OwnerPermissionsClass
from rest_framework.permissions import IsAdminUser


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OwnerPermissionsClass | IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        print(kwargs, request.user.pk)
        return super().retrieve(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = CustomUser.objects.all()
    

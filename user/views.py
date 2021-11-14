from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This email has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)

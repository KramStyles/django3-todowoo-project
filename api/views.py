from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, permissions, response, status
from rest_framework.authtoken.models import Token

from . import serializers
from todo.models import Todo


class TodoCompletedList(generics.ListAPIView):
    serializer_class = serializers.TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
        return todos


class TodoCreate(generics.ListCreateAPIView):
    serializer_class = serializers.TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user, datecompleted__isnull=True)
        return todos

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoOk(generics.UpdateAPIView):
    serializer_class = serializers.TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username = serializer.data['username'])
            token = Token.objects.create(user=user)
            return response.Response({'message': 'User Created', 'token': str(token)}, status=status.HTTP_201_CREATED)
        return response.Response({'message': 'An Error Occurred', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.data['username'], password=serializer.data['password'])
            if user:
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)
                login(request, user=user)
                return response.Response({'message': 'Login Successful', 'token': str(token)}, status=status.HTTP_202_ACCEPTED)
            return response.Response({'message': 'Invalid Authentication'}, status=status.HTTP_403_FORBIDDEN)
        return response.Response({'message': 'An Error Occurred', 'errors': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)

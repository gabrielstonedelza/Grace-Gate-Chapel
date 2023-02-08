from django.shortcuts import get_object_or_404,render
from .models import GGCUser, Profile
from .serializers import UsersSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters

from django.conf import settings

User = settings.AUTH_USER_MODEL

def home(request):
    return render(request, "users/home.html")

class AllUsers(generics.ListCreateAPIView):
    queryset = GGCUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)
#
# @api_view(['GET'])
# @permission_classes([permissions.AllowAny])
# def get_all_user(request):
#     users = User.objects.all()
#     serializer = UsersSerializer(users, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user(request):
    user = GGCUser.objects.filter(username=request.user.username)
    serializer = UsersSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    my_profile = Profile.objects.filter(user=request.user)
    serializer = ProfileSerializer(my_profile, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_my_profile(request):
    my_profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(my_profile, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_username(request):
    user = GGCUser.objects.get(username=request.user.username)
    serializer = UsersSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
@permission_classes([permissions.IsAuthenticated])
def admin_update_user(request,pk):
    user = get_object_or_404(GGCUser,pk=pk)
    serializer = UsersSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_details(request, id):
    user = GGCUser.objects.filter(id=id)
    serializer = UsersSerializer(user, many=True)
    return Response(serializer.data)


# search functioning
class GetAllUsers(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = GGCUser.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'full_name', 'phone_number']
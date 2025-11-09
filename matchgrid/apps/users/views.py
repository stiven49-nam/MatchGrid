from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, UserProfile
from .serializers import UserRegistrationSerializer, UserSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user.profile

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profile__gender', 'profile__city', 'profile__status']
    
    def get_queryset(self):
        # Базовая фильтрация
        queryset = User.objects.all()
        
        # Фильтрация по возрасту
        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')
        
        if min_age:
            queryset = queryset.filter(profile__age__gte=min_age)
        if max_age:
            queryset = queryset.filter(profile__age__lte=max_age)
            
        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def random_profile(request):
    import random
    from django.db.models import Q
    
    # Фильтры из запроса
    gender = request.GET.get('gender')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    city = request.GET.get('city')
    status = request.GET.get('status')
    
    queryset = UserProfile.objects.exclude(user=request.user)
    
    if gender:
        queryset = queryset.filter(gender=gender)
    if min_age:
        queryset = queryset.filter(age__gte=min_age)
    if max_age:
        queryset = queryset.filter(age__lte=max_age)
    if city:
        queryset = queryset.filter(city__iexact=city)
    if status:
        queryset = queryset.filter(status=status)
    
    if queryset.exists():
        random_profile = random.choice(queryset)
        serializer = UserProfileSerializer(random_profile)
        return Response(serializer.data)
    
    return Response({"detail": "Нет подходящих профилей"}, status=status.HTTP_404_NOT_FOUND)
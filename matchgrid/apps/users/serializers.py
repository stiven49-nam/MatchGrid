from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'is_main', 'uploaded_at']

class UserProfileSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    main_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'full_name', 'gender', 'age', 'city', 'hobbies', 
            'status', 'likes_count', 'privacy_settings', 'photos', 'main_photo'
        ]
    
    def get_main_photo(self, obj):
        main_photo = obj.photos.filter(is_main=True).first()
        if main_photo:
            return PhotoSerializer(main_photo).data
        return None

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'profile']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['email']  # Используем email как username
        )
        
        UserProfile.objects.create(user=user, **profile_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'date_joined', 'profile']
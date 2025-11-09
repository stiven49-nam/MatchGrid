from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]
    
    STATUS_CHOICES = [
        ('looking', 'В поиске'),
        ('busy', 'Занят'),
        ('complicated', 'Все сложно'),
        ('not_looking', 'Не ищу'),
    ]
    
    PRIVACY_CHOICES = [
        ('public', 'Публичный'),
        ('private', 'Приватный'),
        ('friends_only', 'Только друзьям'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    city = models.CharField(max_length=100)
    hobbies = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='looking')
    likes_count = models.PositiveIntegerField(default=0)
    privacy_settings = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"

class Photo(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='profile_photos/')
    is_main = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.is_main:
            # Убираем флаг главной фотографии у других фото этого профиля
            Photo.objects.filter(profile=self.profile, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
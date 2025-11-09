from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q
from .models import Interaction, Match, Invitation
from .serializers import InteractionSerializer, MatchSerializer, InvitationSerializer

class InteractionView(generics.CreateAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
        
        # Проверка на взаимный лайк для создания матча
        if serializer.validated_data['action'] == 'like':
            to_user = serializer.validated_data['to_user']
            mutual_like = Interaction.objects.filter(
                from_user=to_user,
                to_user=self.request.user,
                action='like'
            ).exists()
            
            if mutual_like and not Match.objects.filter(
                Q(user1=self.request.user, user2=to_user) | 
                Q(user1=to_user, user2=self.request.user)
            ).exists():
                Match.objects.create(user1=self.request.user, user2=to_user)

class HistoryView(generics.ListAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        action = self.kwargs.get('action')
        return Interaction.objects.filter(
            from_user=self.request.user, 
            action=action
        ).order_by('-created_at')

class LikesHistoryView(generics.ListAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Interaction.objects.filter(
            to_user=self.request.user, 
            action='like'
        ).order_by('-created_at')

class MatchesView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Match.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user),
            is_active=True
        )
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class InvitationView(generics.CreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Проверяем, есть ли матч между пользователями
        to_user = serializer.validated_data['to_user']
        match_exists = Match.objects.filter(
            Q(user1=self.request.user, user2=to_user) | 
            Q(user1=to_user, user2=self.request.user)
        ).exists()
        
        if not match_exists:
            raise serializers.ValidationError("Можно отправлять приглашения только взаимолайкнувшим пользователям")
        
        serializer.save(from_user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_invitation(request, invitation_id, action):
    try:
        invitation = Invitation.objects.get(
            id=invitation_id,
            to_user=request.user,
            status='pending'
        )
    except Invitation.DoesNotExist:
        return Response({"detail": "Приглашение не найдено"}, status=status.HTTP_404_NOT_FOUND)
    
    if action not in ['accept', 'reject']:
        return Response({"detail": "Неверное действие"}, status=status.HTTP_400_BAD_REQUEST)
    
    invitation.status = 'accepted' if action == 'accept' else 'rejected'
    invitation.save()
    
    return Response({"detail": f"Приглашение {action}ed"})
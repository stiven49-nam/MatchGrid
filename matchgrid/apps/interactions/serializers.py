from rest_framework import serializers
from .models import Interaction, Match, Invitation
from matchgrid.apps.users.serializers import UserProfileSerializer

class InteractionSerializer(serializers.ModelSerializer):
    to_user_profile = UserProfileSerializer(source='to_user.profile', read_only=True)
    
    class Meta:
        model = Interaction
        fields = ['id', 'to_user', 'to_user_profile', 'action', 'created_at']
        read_only_fields = ['from_user']

class MatchSerializer(serializers.ModelSerializer):
    other_user_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'other_user_profile', 'created_at', 'is_active']
    
    def get_other_user_profile(self, obj):
        request = self.context.get('request')
        if request and request.user:
            other_user = obj.user2 if obj.user1 == request.user else obj.user1
            return UserProfileSerializer(other_user.profile).data
        return None

class InvitationSerializer(serializers.ModelSerializer):
    from_user_profile = UserProfileSerializer(source='from_user.profile', read_only=True)
    to_user_profile = UserProfileSerializer(source='to_user.profile', read_only=True)
    
    class Meta:
        model = Invitation
        fields = ['id', 'from_user', 'from_user_profile', 'to_user', 'to_user_profile', 
                 'message', 'status', 'created_at', 'updated_at']
        read_only_fields = ['from_user', 'status']
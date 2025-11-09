from django.urls import path
from . import views

urlpatterns = [
    path('interact/', views.InteractionView.as_view(), name='interact'),
    path('history/<str:action>/', views.HistoryView.as_view(), name='history'),
    path('likes-history/', views.LikesHistoryView.as_view(), name='likes-history'),
    path('matches/', views.MatchesView.as_view(), name='matches'),
    path('invitations/', views.InvitationView.as_view(), name='send-invitation'),
    path('invitations/<int:invitation_id>/<str:action>/', views.respond_to_invitation, name='respond-invitation'),
]
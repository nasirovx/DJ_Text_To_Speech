from django.urls import path
from .views import (
    TextToSpeechView, TextToSpeechDetailView, DownloadVoiceView, CreateUserView, CustomObtainAuthToken
)


urlpatterns = [
    path('api-token-auth/', CustomObtainAuthToken.as_view(),name='api_token_auth'),
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('text-to-speech/', TextToSpeechView.as_view(), name='text-to-speech-list'),
    path('text-to-speech/<int:pk>/', TextToSpeechDetailView.as_view(), name='text-to-speech-detail'),
    path('download-voice/<str:file_name>/', DownloadVoiceView.as_view(), name='download-voice'),
]

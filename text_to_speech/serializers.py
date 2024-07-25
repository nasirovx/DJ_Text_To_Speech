from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Text_to_speech


class TextToSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text_to_speech
        fields = ['text', 'file_name']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 
                  'first_name', 'last_name', 'password']

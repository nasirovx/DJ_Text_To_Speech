import io
import re

from gtts import gTTS
from django.utils import timezone
from django.http import FileResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken

from .models import Text_to_speech
from .serializers import TextToSpeechSerializer, UserSerializer


MIN_TEXT_LENGTH = 10
MIN_FILE_NAME_LENGTH = 5
MAX_TEXT_LENGTH = 700
MAX_FILE_NAME_LENGTH = 20


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)
        if created:
            return Response(
                {
                    "token": token.key,
                    "user_id": user.pk,
                    "username": user.username,
                    "message": "Token created",
                }
            )
        else:
            token.created = timezone.now()
            token.save()
            return Response(
                {
                    "token": token.key,
                    "user_id": user.pk,
                    "username": user.username,
                    "message": "Token refreshed",
                }
            )


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class BaseTextToSpeechView(generics.GenericAPIView):
    queryset = Text_to_speech.objects.all()
    serializer_class = TextToSpeechSerializer
    permission_classes = [permissions.IsAuthenticated]

    def validate_request_data(self, text, file_name):
        if not text:
            raise serializers.ValidationError({"error": "Текст не может быть пустым."})
        elif len(text) < MIN_TEXT_LENGTH:
            raise serializers.ValidationError(
                {"error": f"Текст не может быть меньше {MIN_TEXT_LENGTH} символов."}
            )
        elif not file_name:
            raise serializers.ValidationError(
                {"error": "Имя файла не может быть пустым."}
            )
        elif len(file_name) < MIN_FILE_NAME_LENGTH:
            raise serializers.ValidationError(
                {
                    "error": f"Имя файла не может быть меньше {MIN_FILE_NAME_LENGTH} символов."
                }
            )
        elif len(text) > MAX_TEXT_LENGTH:
            raise serializers.ValidationError(
                {"error": f"Текст не может быть больше {MAX_TEXT_LENGTH} символов."}
            )
        elif len(file_name) > MAX_FILE_NAME_LENGTH:
            raise serializers.ValidationError(
                {
                    "error": f"Имя файла не может быть больше {MAX_FILE_NAME_LENGTH} символов."
                }
            )


class TextToSpeechView(BaseTextToSpeechView, generics.ListCreateAPIView):
    def user_text(self, file_name, text, *args, **kwargs):
        match = re.search(r"[\u0400-\u04ff]|[\u0500-\u052f]", text)
        lang = "ru" if match else "en"
        tts = gTTS(text=text, lang=lang)
        voice_bytes = io.BytesIO()
        tts.write_to_fp(voice_bytes)
        voice_bytes.seek(0)

        voice_path = f"voice/{file_name}.mp3"
        with open(voice_path, "wb") as f:
            f.write(voice_bytes.read())

        return voice_path

    def post(self, request, *args, **kwargs):
        text = request.data.get("text")
        file_name = request.data.get("file_name")

        try:
            self.validate_request_data(text, file_name)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            voice_path = self.user_text(file_name, text)
            request.data["voice"] = voice_path
            return super().post(request, *args, **kwargs)


class TextToSpeechDetailView(
    BaseTextToSpeechView, generics.RetrieveUpdateDestroyAPIView
):
    def update_voice(self, file_name, text):
        voice_path = self.user_text(file_name, text)

        self.get_object().voice = voice_path
        self.get_object().save()

    def put(self, request, *args, **kwargs):
        text = request.data.get("text")
        file_name = request.data.get("file_name")

        try:
            self.validate_request_data(text, file_name)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        if self.get_object().created_at is not None:
            raise serializers.MethodNotAllowed("PUT")

        response = super().put(request, *args, **kwargs)

        self.update_voice(file_name, text)

        return response


class DownloadVoiceView(generics.RetrieveAPIView):
    queryset = Text_to_speech.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "file_name"

    def retrieve(self, request, file_name, *args, **kwargs):
        text_to_speech = get_object_or_404(self.get_queryset(), file_name=file_name)
        voice_path = text_to_speech.voice
        response = FileResponse(open(voice_path, "rb"))
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{text_to_speech.file_name}.mp3"'
        return response

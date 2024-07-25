import io
import re

from gtts import gTTS
from django.db import models


class Text_to_speech(models.Model):
    text = models.CharField(
        max_length=700,
        verbose_name="Текст",
        help_text="Введите текст, который вы хотите преобразовать в речь.",
    )
    file_name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Имя файла",
        help_text="Укажите имя аудиофайла.",
    )

    voice = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Голос",
        help_text="Выберите голос для преобразования текста в речь.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания записи.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего обновления записи.",
    )

    def save(self, *args, **kwargs):
        match = re.search(r"[\u0400-\u04ff]|[\u0500-\u052f]", self.text)
        lang = "ru" if match else "en"
        tts = gTTS(text=self.text, lang=lang)
        voice_bytes = io.BytesIO()
        tts.write_to_fp(voice_bytes)
        voice_bytes.seek(0)

        voice_path = f"voice/{self.file_name}.mp3"
        self.voice = voice_path
        with open(voice_path, "wb") as f:
            f.write(voice_bytes.read())

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "Текст в речь"
        verbose_name_plural = "Тексты в речь"

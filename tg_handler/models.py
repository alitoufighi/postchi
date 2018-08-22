from django.db import models


class TelegramPlatform(models.Model):
    username = models.CharField(max_length=100, blank=True)  # username of Telegram channel for showing in profile
    bot_token = models.CharField(max_length=100, blank=True)  # Token given by @BotFather in Telegram
    chat_id = models.CharField(max_length=100, blank=True)  # Numerical chat_id of Telegram channel

    def __str__(self):
        return self.bot_token

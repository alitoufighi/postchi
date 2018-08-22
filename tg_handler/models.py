from django.db import models


class TelegramPlatform(models.Model):
    bot_token = models.CharField(max_length=100, blank=True)  # Token given by @BotFather in Telegram
    # chat_ids = models.ForeignKey(TelegramChatID, on_delete=models.CASCADE, blank=True, related_name='tg_chat_ids')
    #  TODO: FOREIGN KEY ON CHARFIELD DOESNT WORK!
    chat_id = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.bot_token

from django.db import models
from postchiapp import models as core
from post.utils import user_directory_path


class Post(models.Model):
    text = models.TextField(max_length=700, blank=True)
    media = models.FileField(upload_to=user_directory_path, null=True)

    channel = models.ForeignKey(core.Channel, on_delete=models.CASCADE, null=True)  # WHAT TO DO WITH null=True?
    author = models.ForeignKey(core.Account, on_delete=models.DO_NOTHING, null=True)  # CHECK DO_NOTHING

    # If any of fields below is blank, then it is not posted on that platform.
    tg_link = models.URLField(blank=True)
    tw_link = models.URLField(blank=True)
    insta_link = models.URLField(blank=True)

    # TODO: ASK IF IT MAKES SENSE TO DO THIS?:
    # Creating a Platform class which each of TgPlatform, TwPlatform, etc. inherits from it. Platform just pass.
    # and making the `platforms` field above a foreign key to Platform objects :hmm: I just confused.

    def __str__(self):
        return '{text} ...'.format(text=self.text[:50]) if len(self.text) > 50 else self.text

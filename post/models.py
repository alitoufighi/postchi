from django.db import models
from postchiapp import models as core


class Post(models.Model):
    text = models.TextField(max_length=700, blank=True)
    media = models.FileField(null=True)
    author = models.ForeignKey(core.Account, on_delete=models.CASCADE)

    # platforms = ?
    # TODO: ASK IF IT MAKES SENSE TO DO THIS?:
    # Creating a Platform class which each of TgPlatform, TwPlatform, etc. inherits from it. Platform just pass.
    # and making the `platforms` field above a foreign key to Platform objects :hmm: I just confused.

    def __str__(self):
        return '{text} ...'.format(text=self.text[:50] if len(self.text) > 50 else self.text)

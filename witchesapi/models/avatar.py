from django.db import models


class Avatar(models.Model):
    avatar_url = models.URLField()
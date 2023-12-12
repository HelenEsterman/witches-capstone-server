from django.db import models
from django.contrib.auth.models import User


class Witch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='witch')
    avatar = models.ForeignKey("Avatar", on_delete=models.CASCADE, related_name='witch')
    nickname = models.CharField(max_length=200, blank=True)
    coven = models.CharField(max_length=200, blank=True)
    created_on = models.DateField(auto_now_add=True)

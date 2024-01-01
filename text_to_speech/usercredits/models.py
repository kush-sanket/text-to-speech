from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserCredits(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    credits = models.SmallIntegerField(default = 0 , null = False)
    is_premium_user = models.BooleanField(default = False , null = False)
    user_allowed_words = models.SmallIntegerField(default = 1000)

    def save(self, *args, **kwargs):
   
        if self.is_premium_user:
            self.user_allowed_words = 2000
        super().save(*args, **kwargs)
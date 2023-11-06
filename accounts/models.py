from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from core.models import UserApp


class UserAccountTypes(models.TextChoices):
    AUTHOR = 'AUTHOR', 'Author'
    CONSUMER = 'CONSUMER', 'Consumer'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_images', null=True, blank=True)
    user_type = models.CharField(
        max_length=16, choices=UserAccountTypes.choices)
    app_accesses = models.ManyToManyField(UserApp, blank=True)

    def __str__(self) -> str:
        full_name = self.user.get_full_name()
        return f'{full_name.title() if full_name else self.user.email}\'s profile'

# User post save reciever to create profile right after user is created.


def user_post_save_reciever(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile(
            user=instance, user_type=UserAccountTypes.AUTHOR)
        user_profile.save()


post_save.connect(user_post_save_reciever, sender=User)

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Userprofilemodel
import json
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Userprofilemodel.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Userprofilemodel.save()

@receiver(post_save, sender=Userprofilemodel)
def send_onlineStatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.user.username
        user_status = instance.online_status
        
        data = {
            'username': user,
            'status': user_status
        }
        
        async_to_sync(channel_layer.group_send)(
            'user',{
                'type': 'send_onlineStatus',
                'value': json.dumps(data)
            }
        )
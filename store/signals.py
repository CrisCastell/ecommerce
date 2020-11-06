from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User, Group
from .models import Customer, Order
import random

def follower_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(user=instance, username=instance.username, email=instance.email)
    
post_save.connect(follower_profile, sender=User)


def transaction_id(sender, instance, *args, **kwargs):
    if instance.transaction:
        return
    rand = random.randint(1,100000000)

    while(Order.objects.filter(transaction=rand).exists()):
        rand = random.randint(1,100000000)
    
    instance.transaction = rand
pre_save.connect(transaction_id, sender=Order)
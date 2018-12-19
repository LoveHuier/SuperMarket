# _*_coding: utf-8_*_

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserFav


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
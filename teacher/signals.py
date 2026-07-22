from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from .models import Teacher

User = get_user_model()


def _generate_username(email):
    if not email:
        raise ValueError("Email is required to create a user for a Teacher.")
    base = email.split("@")[0]
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}_{suffix}"
        suffix += 1
    return username


def _find_or_create_user(teacher):
    if User.objects.filter(email=teacher.email).exists():
        return User.objects.get(email=teacher.email), False

    username = _generate_username(teacher.email)
    user = User(
        username=username,
        email=teacher.email,
        first_name=teacher.first_name,
        last_name=teacher.last_name,
    )
    user.set_unusable_password()
    user.save()
    return user, True


@receiver(post_save, sender=Teacher)
def create_teacher_user(sender, instance, created, **kwargs):
    if instance.user is not None:
        return

    if not instance.email:
        return

    if kwargs.get("raw"):
        return

    with transaction.atomic():
        user, _ = _find_or_create_user(instance)
        Teacher.objects.filter(pk=instance.pk).update(user=user)
        instance.user = user

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Note, Tag


@receiver(post_save, sender=Tag)
def notify_on_note_create(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Tag '{instance.name}' was created by {instance.owner}")

@receiver(post_save, sender=Tag)
def notify_on_note_update(sender, instance, created, **kwargs):
    if not created:
        print(f"[SIGNAL] Tag '{instance.name}' was updated by {instance.owner}")

@receiver(post_delete, sender=Tag)
def note_deleted(sender, instance, **kwargs):
    print(f"[SIGNAL] Tag '{instance.name}' was deleted by {instance.owner}")


@receiver(post_save, sender=Note)
def notify_on_note_create(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Note '{instance.title}' was created by {instance.owner}")

@receiver(post_save, sender=Note)
def notify_on_note_update(sender, instance, created, **kwargs):
    if not created:
        print(f"[SIGNAL] Note '{instance.title}' was updated by {instance.owner}")

@receiver(post_delete, sender=Note)
def note_deleted(sender, instance, **kwargs):
    print(f"[SIGNAL] Note '{instance.title}' was deleted by {instance.owner}")
    
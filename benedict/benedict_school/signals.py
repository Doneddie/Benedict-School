from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Child, PupilApplication

@receiver(post_save, sender=Child)
def create_pupil_application(sender, instance, created, **kwargs):
    """
    Signal to automatically create a PupilApplication when a new Child is registered.
    """
    if created:
        # Check if the child is newly created
        PupilApplication.objects.create(child=instance)
        print(f"PupilApplication created for child: {instance.name}")

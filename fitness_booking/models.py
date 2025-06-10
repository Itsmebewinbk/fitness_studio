from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



class AbstractModel(models.Model):

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True


class FitnessClass(AbstractModel):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    total_slots = models.PositiveIntegerField(default=0)
    available_slots = models.PositiveIntegerField()

  

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.datetime}"



@receiver(post_save, sender=FitnessClass)
def set_available_slots_on_create(sender, instance, created, **kwargs):
    # if settings.SIGNAL_ENABLE:
        if created and instance.available_slots != instance.total_slots:
            instance.total_slots = instance.available_slots
            instance.save(update_fields=["total_slots"])

class Booking(AbstractModel):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"

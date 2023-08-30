from django.db import models
from django.core.validators import MinValueValidator

class Material(models.Model):
    TYPE_CHOICES = [
        ('doors_windows', 'Doors and Windows'),
        ('construction_materials', 'Construction Materials'),
        ('other', 'Other')
    ]

    name = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True) #(upload_to='recipes/', blank=True)
    description = models.TextField(max_length=200, blank=True)
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1,
            message='Minimum amount of mateerials 1'),),
        blank=True)
    availability = models.BooleanField(default=False)
    type = type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='other'
    )

    def __str__(self):
        return self.name
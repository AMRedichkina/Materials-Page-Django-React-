from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

class Material(models.Model):
    """
    Model representing a material with related information.

    This model represents a material entity in the application. It includes
    fields for name, image, description, amount, availability, and type.

    Attributes:
        TYPE_CHOICES (list of tuples): Choices for the 'type' field.
        name (TextField): Name of the material.
        image (ImageField): Image associated with the material.
        description (TextField): Description of the material.
        amount (PositiveSmallIntegerField): Amount of the material available.
        availability (BooleanField): Availability status of the material.
        type (CharField): Type of the material (e.g., doors, windows, etc.).

    Methods:
        __str__(): Returns the string representation of the material.
        save(*args, **kwargs): Overrides the default save method to update
            availability and send messages to WebSocket consumers.
    """

    TYPE_CHOICES = [
        ('doors', 'Doors'),
        ('windows', 'Windows'),
        ('bricks', 'Bricks'),
        ('blocks', 'Blocks'),
        ('other', 'Other')
    ]

    name = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True)
    description = models.TextField(max_length=200, blank=True)
    amount = models.PositiveSmallIntegerField(blank=True)
    availability = models.BooleanField(default=False)
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='other'
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Determine if the object is being created or updated
        is_new = not self.pk

        # Update the availability based on the amount
        if self.amount == 0:
            self.availability = False
        else:
            self.availability = True

        # Call the original save method
        super().save(*args, **kwargs)
        
        # Get the channel layer for sending messages to WebSocket consumers
        channel_layer = get_channel_layer()

        # Prepare the content of the message to be sent
        message_content = {
            'id': self.id,
            'name': self.name,
            'image': self.image.url if self.image else None,
            'description': self.description,
            'amount': self.amount,
            'availability': self.availability,
            'type': self.type
        }

        if is_new:
            message_type = 'new_material'
        else:
            message_type = 'update_material_status'

         # Send the message to the 'material_status' group
        async_to_sync(channel_layer.group_send)(
            'material_status',
            {
                'type': message_type,
                'text': message_content
            }
        )

        # Log the information about the sent message
        logger.info(f"Sent {message_type} message for Material ID {self.id}")
        logger.info(f"Message content: {message_content}")
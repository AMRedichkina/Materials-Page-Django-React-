"""
Command to load materials data from JSON and associated images into the database.

This script reads a JSON file containing material data, including names, descriptions,
amounts, and image file paths. It then processes the data, creates or updates Material
objects in the database, and associates images with the materials.

Usage: python manage.py load_materials <filename>

Args:
    filename (str): The name of the JSON file containing material data.

Example:
    python manage.py load_materials material_data.json
"""


import json
import os
import io  
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core import exceptions
from api.models import Material
from PIL import Image
from django.core.files import File

import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')
MAX_SIZE = 800

class Command(BaseCommand):
    help = 'Loading materials from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='material_list.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        """
        Handle the command to load materials data into the database.
        """
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                    encoding='utf-8') as f:
                data = json.load(f)

                for item in data:
                    try:
                        original_name = item["name"]

                        material, created = Material.objects.get_or_create(
                            name=item["name"],
                            defaults={
                                'description': item["description"],
                                'amount': item["amount"],
                                'availability': True
                            }
                        )

                        image_path = os.path.join(DATA_ROOT, "images", original_name + ".png")
                        
                        with open(image_path, 'rb') as img_file:
                            image_bytes = img_file.read()

                        with Image.open(io.BytesIO(image_bytes)) as img:
                            if img.height > MAX_SIZE or img.width > MAX_SIZE:
                                output_io_stream = io.BytesIO()
                                img.thumbnail((MAX_SIZE, MAX_SIZE))
                                img.save(output_io_stream, format='PNG', quality=85)
                                image_file = File(output_io_stream, name=original_name + ".png")
                            else:
                                image_file = File(io.BytesIO(image_bytes), name=original_name + ".png")

                            material.image = image_file

                        if not created:
                            material.description = item["description"]
                            material.amount = item["amount"]
                            material.availability = True  

                        material.save()

                    except exceptions.FieldError as e:
                        logger.error(f"Error with material {item['name']}: {str(e)}")
                    except Exception as e:
                        logger.error(f"Unknown error with material {item['name']}: {str(e)}")

        except FileNotFoundError:
            raise CommandError(f"Error occurred for material '{item['name']}'. Please check the file path.")

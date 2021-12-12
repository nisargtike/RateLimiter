from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image as IMAGE
from io import BytesIO

import uuid
import logging
import sys
import json

logger = logging.getLogger(__name__)


class CustomUser(User):

    def save(self, *args, **kwargs):
        
        if self.pk == None:
            self.set_password(self.password)
            
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
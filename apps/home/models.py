# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Splint(models.Model):
    id_splint = models.CharField(primary_key=True,max_length=200)
    splint_file = models.FileField(upload_to='apps/home/media/splints', blank=False, null=False)
    id_user = models.ForeignKey(
        User,
        models.CASCADE,
        unique=False,
        null=False,
        blank=False,
        default=1
    )
    class Meta:
        managed = True
        db_table = "Splint"
        verbose_name_plural = "Splints"
        indexes = [
            models.Index(
                fields=[
                    "id_splint",
                ]
            ),
        ]
    
    def __str__(self):
        return f"Splint {self.id_splint}"
# Create your models here.


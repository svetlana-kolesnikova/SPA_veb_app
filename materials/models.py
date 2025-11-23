#  materials/models.py
from decimal import Decimal

from django.conf import settings
from django.db import models


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(max_length=150)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses", null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Цена курса")

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons", null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Цена урока")

    def __str__(self):
        return self.name

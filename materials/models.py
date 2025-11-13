#  materials.py
from django.db import models


class Course(models.Model):
    """Модель курса"""
    name = models.CharField(max_length=150)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока"""
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

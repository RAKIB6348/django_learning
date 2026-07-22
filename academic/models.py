from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=50)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')

    class Meta:
        unique_together = ('name', 'class_ref')

    def __str__(self):
        return f"{self.class_ref} - Section {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.class_ref})"

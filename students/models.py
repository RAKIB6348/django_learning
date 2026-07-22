from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    father_name = models.CharField(max_length=100, default='')
    mother_name = models.CharField(max_length=100, default='')
    parent_phone = models.CharField(max_length=15, default='')
    parent_email = models.EmailField(blank=True)
    parent_address = models.TextField(blank=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

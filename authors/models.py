from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='authors_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
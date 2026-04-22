from django.db import models


class Brand(models.Model):

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Flavor(models.Model):

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Chips(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    flavors = models.ManyToManyField(Flavor)
    image = models.ImageField(upload_to='chips_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"
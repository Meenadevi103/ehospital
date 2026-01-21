from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    resources = models.TextField() # List of resources
    
    def __str__(self):
        return self.name

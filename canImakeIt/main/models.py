from django.db import models
from django.contrib.auth.models import User

class Kitchen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kitchen', null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

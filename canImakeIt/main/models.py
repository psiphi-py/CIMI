# basic django models incorporated into CIMI
from django.db import models
from django.contrib.auth.models import User

class Kitchen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kitchen', null=True)
    name = models.CharField(max_length=100)

# display data in human form
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    # created an instance of Kitchen to link user's unique data for unique content viewing
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    #text = ingredient name
    text = models.CharField(max_length=200)
    # checkbox for ingredient selection
    complete = models.BooleanField()

# display data in human form
    def __str__(self):
        return self.text

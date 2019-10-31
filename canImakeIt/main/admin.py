from django.contrib import admin
from .models import Kitchen, Ingredient

# models that may be altered via django admin page
admin.site.register(Kitchen)
admin.site.register(Ingredient)

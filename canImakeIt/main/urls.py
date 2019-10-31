from django.urls import path
from . import views
# function based views as debugging resources more reachable
# linking templates with views

urlpatterns = [
    # <int:id> = dynamic templates for user unique views via their created data id
    path('<int:id>', views.index, name='index'),
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('view/', views.view, name='view'),
    path('existing/', views.create, name='existing'),
    path('delete/', views.delete, name='delete'),
    path('allrecipes/', views.allrecipes, name='allrecipes'),
    path('foodnetwork/', views.foodnetwork, name='foodnetwork'),
    path('food_com/', views.food_com, name='food_com'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
]
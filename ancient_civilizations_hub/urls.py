"""Defines URL patterns for ancient_civilizations_hub."""

from django.urls import path

from . import views

app_name = 'ancient_civilizations_hub'
urlpatterns = [
        # Home Page
        path('', views.index, name='index'),
        # Page that shows all civilizations.
        path('civilizations/', views.civilizations, name='civilizations'),
        # Detail page for a single civilization. 
        path('civilizations/<int:civilization_id>/', views.civilization, name='civilization'),
        # Page for adding a new civilization
        path('new_civilization/', views.new_civilization, name='new_civilization'),
        # Page for adding a new entry
        path('new_civilization/<int:civilization_id>/', views.new_entry, name='new_entry'),
        # Page for editing an entry.
        path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
  

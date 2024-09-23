from django.urls import path
from . import views

urlpatterns = [
    path('transformator/add/', views.transformator_add, name='add_transformator'),
    path('transformator/', views.transformator_list, name='transformator_list'),
    path('transformator/edit/<int:pk>/', views.transformator_edit, name='edit_transformator'),
    path('transformator/delete/<int:pk>/', views.transformator_delete, name='delete_transformator'),
]

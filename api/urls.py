from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/', views.addData),
      path('update/<int:pk>/', views.updateData),
    path('delete/<int:pk>/', views.deleteData),
]

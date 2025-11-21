from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/data/<str:img_name>/', views.get_image_data, name='get_image_data'),
    path('api/save/', views.save_verified_data, name='save_verified_data'),
]

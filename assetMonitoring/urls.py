from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_asset/', views.create_asset, name='create_asset'),
    path('update_asset/<int:asset_id>', views.update_asset, name='update_asset'),
    path('delete_asset/<int:asset_id>', views.delete_asset, name='delete_asset'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
]
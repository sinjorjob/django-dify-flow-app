from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('run_dify_workflow/', views.run_dify_workflow, name='run_dify_workflow'),
]
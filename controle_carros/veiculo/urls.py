from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_carro, name='criar_carro'),
    path('editar/<int:carro_id>/', views.editar_carro, name='editar_carro'),
    path('excluir/<int:carro_id>/', views.excluir_carro, name='excluir_carro'),
]

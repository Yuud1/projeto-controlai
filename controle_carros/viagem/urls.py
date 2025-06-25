from django.urls import path
from . import views

urlpatterns = [
    path('nova/', views.nova_viagem, name='nova_viagem'),
    path('editar/<int:viagem_id>/', views.editar_viagem, name='editar_viagem'),
    path('excluir/<int:viagem_id>/', views.excluir_viagem, name='excluir_viagem'),
]

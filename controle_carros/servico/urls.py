from django.urls import path
from . import views

urlpatterns = [
    path('novo/', views.novo_servico, name='novo_servico'),
    path('editar/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:servico_id>/', views.excluir_servico, name='excluir_servico'),
]

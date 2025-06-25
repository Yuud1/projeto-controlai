from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('dashboard/', views.dashboard_usuario, name='dashboard_usuario'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard-admin/criar-usuario/', views.criar_usuario, name='dashboard_admin_criar_usuario'),
    path('dashboard-admin/editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('dashboard-admin/excluir-usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
]

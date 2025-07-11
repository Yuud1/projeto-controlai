from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sistema.urls')),
    path('veiculo/', include('veiculo.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('viagens/', include('viagem.urls')),
    path('servicos/', include('servico.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Serve para arquivos estáticos e de mídia durante o desenvolvimento (caminho)




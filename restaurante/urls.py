from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs do seu app principal
    path('', include('guests.urls')),

    # URLs de autenticação (login, logout, reset de senha, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('pedidos/', include('pedidos.urls')),  

    path('financeiro/', include('financeiro.urls')),
    path('estoque/', include('estoque.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




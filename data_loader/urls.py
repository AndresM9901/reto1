from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'conexiones', ConexionViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'sesiones', SessionUsuarioViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'ruta_ubicaciones', RutaUbicacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ubicaciones1/', UbicacionCreateView.as_view(), name='ubicacion-create'),
    path('conexiones1/', ConexionCreateView.as_view(), name='conexion-create'),
    path('shortest_route/', shortest_route, name='shortest_route')
]

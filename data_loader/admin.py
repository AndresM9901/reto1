from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Conexion)
class ConexionAdmin(admin.ModelAdmin):
    list_display = ['ubicacion1', 'ubicacion2', 'peso']

admin.site.register(Ubicacion)
admin.site.register(Usuario)
admin.site.register(SessionUsuario)
admin.site.register(Ruta)
admin.site.register(RutaUbicacion)
# admin.site.register(CustomUser)
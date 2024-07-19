from django.db import models

# Create your models here.
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    posX = models.IntegerField()
    posY = models.IntegerField()
    
class Conexion(models.Model):
    ubicacion1 = models.ForeignKey(Ubicacion, related_name='conexiones_origen', on_delete=models.CASCADE)
    ubicacion2 = models.ForeignKey(Ubicacion, related_name='conexiones_destino', on_delete=models.CASCADE)
    peso = models.IntegerField()
    
class Usuario(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    email_confirmado = models.BooleanField(default=False)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    
class SessionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_session = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
class Ruta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    origen = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    
class RutaUbicacion(models.Model):
    ruta = models.ForeignKey(Ruta, related_name='ruta_ubicaciones', on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    orden = models.IntegerField()
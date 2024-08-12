from django.db import models

# Create your models here.
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    posX = models.IntegerField()
    posY = models.IntegerField()
    
    def __str__(self):
        return f'{self.nombre}'
    
class Conexion(models.Model):
    ubicacion1 = models.ForeignKey(Ubicacion, related_name='conexiones_origen', on_delete=models.CASCADE)
    ubicacion2 = models.ForeignKey(Ubicacion, related_name='conexiones_destino', on_delete=models.CASCADE)
    peso = models.IntegerField()
    
    class Meta:
        unique_together = ('ubicacion1', 'ubicacion2')
    
    def __str__(self):
        return f'{self.ubicacion1} -> {self.ubicacion2}, {self.peso}'
    
class Usuario(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    email_confirmado = models.BooleanField(default=False)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.email}'
    
class SessionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_session = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    def __str__(self):
        return f'{self.usuario}'
    
class Ruta(models.Model):
    inicio = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.usuario}'
    
class RutaUbicacion(models.Model):
    ruta = models.ForeignKey(Ruta, related_name='ruta_ubicaciones', on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    orden = models.IntegerField()
    
    def __str__(self):
        return f'{self.ruta}'
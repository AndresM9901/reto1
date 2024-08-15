from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

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
    

# class Usuario(models.Model):
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     email_confirmado = models.BooleanField(default=False)
#     last_ip = models.GenericIPAddressField(null=True, blank=True)
    
#     def __str__(self):
#         return f'{self.email}'
    
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
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El correo electronico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
  

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    email_confirmado = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    verification_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    session_date = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
    
class SessionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_session = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    def __str__(self):
        return f'{self.usuario}'
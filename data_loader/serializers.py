from rest_framework import serializers
from .models import Ubicacion, Conexion, Usuario, SessionUsuario, Ruta, RutaUbicacion

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class ConexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conexion
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class SessionUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionUsuario
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class RutaUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaUbicacion
        fields = '__all__'
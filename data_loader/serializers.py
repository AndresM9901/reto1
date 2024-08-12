from rest_framework import serializers
from .models import *

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ['id', 'nombre', 'posX', 'posY']

class ConexionSerializer(serializers.ModelSerializer):
    ubicacion1 = serializers.PrimaryKeyRelatedField(queryset=Ubicacion.objects.all())
    ubicacion2 = serializers.PrimaryKeyRelatedField(queryset=Ubicacion.objects.all())

    class Meta:
        model = Conexion
        fields = ['ubicacion1', 'ubicacion2', 'peso']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class SessionUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionUsuario
        fields = '__all__'

# class RutaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ruta
#         fields = '__all__'

class RutaUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaUbicacion
        fields = '__all__'
        
class RutaSerializer(serializers.Serializer):
    ubicaciones = UbicacionSerializer(many=True)
    conexiones = ConexionSerializer(many=True)
    inicio = serializers.CharField()
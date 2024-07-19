from .models import *
from .serializers import *
from allauth.account.views import ConfirmEmailView
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

# Create your views here.
class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class ConexionViewSet(viewsets.ModelViewSet):
    queryset = Conexion.objects.all()
    serializer_class = ConexionSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class SessionUsuarioViewSet(viewsets.ModelViewSet):
    queryset = SessionUsuario.objects.all()
    serializer_class = SessionUsuarioSerializer

    @action(detail=True, methods=['post'])
    def validate_session(self, request, pk=None):
        usuario = self.get_object()
        session = SessionUsuario.objects.get(usuario.usuario)
        ip_address = request.META['REMOTE_ADDR']
        
        if session.ip_address != ip_address:
            session.ip_address = ip_address
            session.save()
            return Response({
                "message": "Sesion validada."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Sesion ya iniciada desde esta IP."
            }, status=status.HTTP_200_OK)

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class RutaUbicacionViewSet(viewsets.ModelViewSet):
    queryset = RutaUbicacion.objects.all()
    serializer_class = RutaUbicacionSerializer

class CustomConfirmEmailView(ConfirmEmailView):
    @csrf_exempt
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        user = get_user_model().objects.get(email=self.object.email_address.email)
        redirect_url = reverse('user', args=(user.id,))
        return redirect(redirect_url)
from .models import *
from .serializers import *
from .utils.graph_algorithms import get_graph, dijkstra
from allauth.account.models import EmailConfirmation
from allauth.account.views import ConfirmEmailView
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

# Create your views here.
class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class ConexionViewSet(viewsets.ModelViewSet):
    queryset = Conexion.objects.all()
    serializer_class = ConexionSerializer

# class UsuarioViewSet(viewsets.ModelViewSet):
#     queryset = Usuario.objects.all()
#     serializer_class = UsuarioSerializer

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
    
class UbicacionCreateView(APIView):
    def post(self, request, format=None):
        serializer = UbicacionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConexionCreateView(APIView):
    def post(self, request, format=None):
        conexiones_data = request.data

        # Primero, verifica si las ubicaciones existen y obtén sus IDs
        ubicaciones = Ubicacion.objects.filter(nombre__in=[c['ubicacion1'] for c in conexiones_data] + [c['ubicacion2'] for c in conexiones_data])
        ubicaciones_dict = {u.nombre: u.id for u in ubicaciones}
        # print(ubicaciones_dict)

        # Reemplaza nombres por IDs
        for c in conexiones_data:
            c['ubicacion1'] = ubicaciones_dict.get(c['ubicacion1'])
            # print(ubicaciones_dict.get(c['ubicacion1']))
            c['ubicacion2'] = ubicaciones_dict.get(c['ubicacion2'])

        print(f'1: {conexiones_data}, 2: {ubicaciones_dict}')
        serializer = ConexionSerializer(data=conexiones_data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@require_http_methods(["GET"])
def shortest_route(request):
    start_name = request.GET.get('start')
    end_name = request.GET.get('end')
    
    if not start_name or not end_name:
        return JsonResponse({"error": "Ambos nombres deben ingresarsen"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        start = Ubicacion.objects.get(nombre=start_name)
        end = Ubicacion.objects.get(nombre=end_name)
    except Ubicacion.DoesNotExist:
        return JsonResponse({"error": "Una o las dos rutas no existe en la base de datos"}, status=status.HTTP_400_BAD_REQUEST)
    
    graph = get_graph()
    ruta, distancia = dijkstra(graph, start.nombre, end.nombre)
    
    return JsonResponse({
        "ruta": ruta,
        "distancia": distancia
    })

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        key = kwargs["key"]
        print(f"{self}")
        print(f"{request}")
        print(f"{args}")
        print(f"{kwargs}")

        try:
            email_confirmation = EmailConfirmation.objects.get(key=key)
            print(email_confirmation)
            email_confirmation.confirm(request)

        except EmailConfirmation.DoesNotExist:
            return JsonResponse({"error": "Confirmacion invalida"}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"success": "Confirmacion correcta"}, status=status.HTTP_201_CREATED)

# class RegistrarUsuario(APIView):
#     def post(self, request):
#         if request.method == "POST":


class UserRegistrationView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR')
        user = serializer.save(ip_address=ip_address)
        print(user.verification_key)
        # confirmation_link = self.request.build_absolute_url(reverse('verify_email', args=[uid, token]))
        confirmation_link = self.request.build_absolute_uri(reverse('verify_email', args=[user.verification_key]))

        subject = 'Confirma tu correo electrónico'
        message = render_to_string('email/confirmation_email.html', {
            'user': user,
            'confirmation_link': confirmation_link
        })
        send_mail(subject, message, None, [user.email])
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        print(user.email_confirmado)

        if not user.email_confirmado:
            raise serializers.ValidationError({"detail": "Correo electrónico sin verificar. Por favor, verifica tu correo primero"}, code=status.HTTP_403_FORBIDDEN)

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
    
def verify_email(request, verification_key):
    user = get_object_or_404(Usuario, verification_key=verification_key)

    if not user.email_confirmado:
        user.email_confirmado = True
        user.verification_key = None
        user.save()
        return JsonResponse({"message": "Correo ha sido confirmado correctamente"}, status=status.HTTP_200_OK)
    
    else:
        return JsonResponse({"message": "El correo ya ha sido confirmado"})

@csrf_exempt   
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(email=email, password=password)

    if user is None:
        return JsonResponse({"message": "Cuenta no activa con las credenciales dadas"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.email_confirmado:
        return JsonResponse({"message": "Correo no confirmado"}, status=status.HTTP_401_UNAUTHORIZED)

    current_ip = request.META.get('REMOTE_ADDR')
    if user.ip_address and user.ip_address != current_ip:
        user.ip_address = current_ip
        user.session_date = timezone.now()
        user.save()
    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse({
        "user": {
            "email": user.email,
            "ip_address": user.ip_address,
            "session_date": user.session_date
        },
        "access": f'Bearer {access_token}'
    })
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Company, Employee, Client, Product, Invoice, InvoiceDetail, Inventory
from .serializers import (
    CompanySerializer,
    EmployeeSerializer,
    ClientSerializer,
    ProductSerializer,
    InvoiceSerializer,
    InvoiceDetailSerializer,
    InventorySerializer,
)
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status


# Permiso personalizado para permitir solo lectura a usuarios no autenticados
class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Permite acceso de lectura a cualquier usuario,
    pero requiere autenticación para crear, actualizar o eliminar.
    """
    def has_permission(self, request, view):
        # Métodos seguros (GET, HEAD, OPTIONS) permitidos para cualquiera
        if request.method in SAFE_METHODS:
            return True
        # Requiere autenticación para métodos como POST, PUT, PATCH, DELETE
        return request.user and request.user.is_authenticated

class TokenProvider(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': EmployeeSerializer(user).data  # Devuelve los datos del usuario autenticado
        }, status=status.HTTP_200_OK)


# ViewSet para el modelo Company
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


# ViewSet para el modelo Employee
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para el modelo Client
class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para el modelo Product
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        # Hacer que la actualización sea parcial por defecto
        partial = kwargs.pop('partial', True)
        instance = self.get_object()  # Obtener la instancia a actualizar
        datos = request.data.copy()  # Crear una copia de los datos enviados

        # Eliminar campos vacíos del payload
        if datos.get('image1') == '':
            datos.pop('image1')
        if datos.get('image2') == '':
            datos.pop('image2')
        if datos.get('image3') == '':
            datos.pop('image3')
        if datos.get('image4') == '':
            datos.pop('image4')
        if datos.get('image5') == '':
            datos.pop('image5')
        if datos.get('image6') == '':
            datos.pop('image6')

        # Serializar y validar los datos actualizados
        serializer = self.get_serializer(instance, data=datos, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Actualizar la instancia
        self.perform_update(serializer)

        # Retornar la instancia actualizada
        return Response(serializer.data)


# ViewSet para el modelo Invoice
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para el modelo InvoiceDetail
class InvoiceDetailViewSet(ModelViewSet):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para el modelo Inventory
class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]


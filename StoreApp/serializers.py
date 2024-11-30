from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Company, Employee, Client, Product, Invoice, InvoiceDetail, Inventory
from drf_extra_fields.fields import Base64ImageField

# Serializador para el modelo Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# Serializador para el modelo Employee
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['password']  # Excluye la contraseña de la respuesta

    def create(self, validated_data):
        user = Employee(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            direccion=validated_data['direccion'],
            username=validated_data['username'],
            telefono=validated_data['telefono'],
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            is_superuser=validated_data['is_superuser'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Serializador para el modelo Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['password']  # Excluye la contraseña de la respuesta

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


# Serializador para el modelo Product
class ProductSerializer(serializers.ModelSerializer):
    # Campos de imágenes usando Base64ImageField
    image1 = Base64ImageField(required=True)
    image2 = Base64ImageField(required=False)
    image3 = Base64ImageField(required=False)
    image4 = Base64ImageField(required=False)
    image5 = Base64ImageField(required=False)
    image6 = Base64ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'


# Serializador para el modelo Invoice
class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


# Serializador para el modelo InvoiceDetail
class InvoiceDetailSerializer(serializers.ModelSerializer):
    invoice = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = InvoiceDetail
        fields = '__all__'


# Serializador para el modelo Inventory
class InventorySerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'

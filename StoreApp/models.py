from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


# Modelo de la empresa, incluye información general como nombre, dirección, teléfono, etc.
class Company(models.Model):
    name = models.CharField(max_length=50)  # Razón social
    address = models.CharField(max_length=100)  # Dirección
    phone = models.CharField(max_length=20)  # Teléfono
    email = models.EmailField(max_length=100)  # Correo electrónico
    website = models.URLField(max_length=100, blank=True, null=True)  # Sitio web
    tax_id = models.CharField(max_length=20, unique=True)  # NIT
    legal_representative = models.CharField(max_length=100)  # Representante legal

    def __str__(self):
        return self.name


# Modelo del empleado, hereda de AbstractUser para utilizar el sistema de autenticación de Django.
class Employee(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='employees', null=True, blank=True ) 
    address = models.CharField(max_length=100, blank=True, null=True)  # Dirección
    phone = models.CharField(max_length=20, blank=True, null=True)  # Teléfono
    position = models.CharField(max_length=50, blank=True, null=True)  # Cargo o posición
    token = models.CharField(max_length=100,null=True,blank=True,default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Modelo del cliente, extiende funcionalidades para incluir contraseñas.
class Client(models.Model):
    first_name = models.CharField(max_length=50)  # Nombre
    last_name = models.CharField(max_length=50)  # Apellido
    address = models.CharField(max_length=100)  # Dirección
    phone = models.CharField(max_length=20)  # Teléfono
    email = models.EmailField(max_length=100, unique=True)  # Correo electrónico
    username = models.CharField(max_length=128, unique=True)  # Nombre de usuario
    password = models.CharField(max_length=128)  # Contraseña
    token = models.CharField(max_length=100,null=True,blank=True,default='')

    def save(self, *args, **kwargs):
        # Hash de la contraseña antes de guardar
        if not self.pk:  # Solo se hashea si es una nueva instancia
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Modelo del producto, incluye detalles como precio, stock, descripción y múltiples imágenes.
class Product(models.Model):
    name = models.CharField(max_length=50)  # Nombre del producto
    description = models.TextField()  # Descripción
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Descuento
    stock = models.PositiveIntegerField()  # Cantidad en inventario
    color = models.CharField(max_length=50, blank=True, null=True)  # Color
    category = models.CharField(max_length=100, blank=True, null=True)  # Categoría
    product_type = models.CharField(max_length=100, blank=True, null=True) # Categoria.
    fragrance = models.CharField(max_length=100, blank=True, null=True)  # Fragancia o aroma
    size = models.CharField(max_length=50, blank=True, null=True)  # Tamaño
    weight = models.PositiveIntegerField(help_text="Weight in grams", blank=True, null=True)  # Peso en gramos
    duration = models.PositiveIntegerField(help_text="Duration in hours", blank=True, null=True)  # Duración en horas
    materials = models.TextField(blank=True, null=True)  # Materiales del producto
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)  # Imagen 1
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)  # Imagen 2
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)  # Imagen 3
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)  # Imagen 4
    image5 = models.ImageField(upload_to='products/', blank=True, null=True)  # Imagen 5
    image6 = models.ImageField(upload_to='products/', blank=True, null=True)  # Imagen 6

    def __str__(self):
        return self.name


# Modelo de la factura, relaciona un cliente y almacena la fecha de la venta.
class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='invoices')  # Cliente asociado
    sale_date = models.DateTimeField(auto_now_add=True)  # Fecha de la venta

    def __str__(self):
        return f"Invoice #{self.id} - Client: {self.client.first_name} {self.client.last_name}"


# Modelo del detalle de la factura, vincula los productos con las facturas y almacena cantidades y totales.
class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='details')  # Factura asociada
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='invoice_details')  # Producto asociado
    quantity = models.PositiveIntegerField()  # Cantidad de productos
    total_value = models.DecimalField(max_digits=10, decimal_places=2)  # Valor total

    def __str__(self):
        return f"Invoice Detail #{self.invoice.id} - Product: {self.product.name}"


# Modelo del inventario, vincula productos con la empresa y su cantidad disponible.
class Inventory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='inventories')  # Empresa asociada
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='inventories')  # Producto asociado
    quantity = models.PositiveIntegerField()  # Cantidad en inventario
    unit_value = models.DecimalField(max_digits=10, decimal_places=2)  # Valor unitario

    def __str__(self):
        return f"Inventory for {self.company.name} - Product: {self.product.name}"

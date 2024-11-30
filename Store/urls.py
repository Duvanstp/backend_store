from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Importa tus ViewSets
from StoreApp.views import (
    CompanyViewSet,
    EmployeeViewSet,
    ClientViewSet,
    ProductViewSet,
    InvoiceViewSet,
    InvoiceDetailViewSet,
    InventoryViewSet,
    TokenProvider,
)

# Configuración del esquema de la API
schema_view = get_schema_view(
    openapi.Info(
        title="Store API",
        default_version='v1',
        description="Documentación de la API para el proyecto Store",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soporte@store.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configuración del router
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-details', InvoiceDetailViewSet, basename='invoice-detail')
router.register(r'inventories', InventoryViewSet, basename='inventory')

# Configuración de las rutas
urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('api/', include(router.urls)),  # Rutas de la API
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # Esquema JSON o YAML
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Redoc
    path('api/token/', TokenProvider.as_view(), name='token_provider'),
]

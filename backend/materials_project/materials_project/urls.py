from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import MaterialViewSet
from djoser.views import UserViewSet

# Create a router for managing API endpoints
router = routers.DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'users', UserViewSet)

# Define the schema view for API documentation
schema_view = get_schema_view(openapi.Info(
                              title="Materials Project",
                              default_version='v1',
                              description=('''API Documentation'''),
                              contact=openapi.Contact(email="admin@admin.ru"),
                              license=openapi.License(name="BSD License"),
                              ),
                              public=True,
                              permission_classes=(permissions.AllowAny,),
                              )


# URL patterns for different endpoints
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin site
    path('api/', include(router.urls)),  # API endpoints registered using the router
    path('api/', include('djoser.urls')),  # Djoser authentication endpoints
    path('api/auth/', include('djoser.urls.authtoken')),  # Djoser token authentication
    path('__debug__/', include('debug_toolbar.urls')),  # Debug toolbar for debugging

    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),  # Swagger JSON schema
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),  # Swagger UI
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),  # ReDoc documentation
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development



# If in DEBUG mode, serve static files as well
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
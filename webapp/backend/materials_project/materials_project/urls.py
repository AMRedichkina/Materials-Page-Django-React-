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

router = routers.DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'users', UserViewSet)

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('__debug__/', include('debug_toolbar.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
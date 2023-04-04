from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from api.swagger import swagger_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path("api/", include("api.urls")),
    path('admin/', admin.site.urls),
]

# swagger
urlpatterns += [
   path('swagger/',
         swagger_schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'
         ),
    path('redoc/',
         swagger_schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'
         ),
]

urlpatterns += [re_path(r"^.*", TemplateView.as_view(template_name="index.html"))]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
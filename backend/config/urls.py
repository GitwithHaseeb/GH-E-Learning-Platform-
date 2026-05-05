"""
Root URLconf — API versioning `/api/v1/...` aur schema docs.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/", include(("core.api_urls", "api"), namespace="v1")),
    path("api/v2/", include(("core.api_urls", "api"), namespace="v2")),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import os

    if os.environ.get("ENABLE_DEBUG_TOOLBAR", "").lower() in ("1", "true", "yes"):
        try:
            import debug_toolbar

            urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
        except ImportError:
            pass

admin.site.site_header = "E-Learning Admin"
admin.site.site_title = "E-Learning"

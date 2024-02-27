
from django.contrib import admin
from django.conf import settings  # new
from django.urls import path, include  # new
from django.conf.urls.static import static  # new


urlpatterns = [
    path('mohammadmin/', admin.site.urls),
    path('',include('base.urls')),
    path('',include('members.urls')),
    path('', include("django.contrib.auth.urls")),
    path('products/',include('products.urls')),
    path('api/',include('api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
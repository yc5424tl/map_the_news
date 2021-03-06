"""mtn_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset",),
    path("admin/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done",),
    path("reset/<uid64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset-confirm",),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete",),
    path("", include("mtn_web.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = "mtn_web.views.handler400"
handler401 = "mtn_web.views.handler401"
handler403 = "mtn_web.views.handler403"
handler404 = "mtn_web.views.handler404"
handler500 = "mtn_web.views.handler500"


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

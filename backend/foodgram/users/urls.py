from django.urls import include, path
from rest_framework import routers

from users.views import CustomUserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('users/', include(router.urls)),
]

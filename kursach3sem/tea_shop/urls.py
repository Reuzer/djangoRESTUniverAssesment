from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeaCategoryViewSet, TeaProductViewSet

router = DefaultRouter()
router.register(r'categories', TeaCategoryViewSet, basename='category')
router.register(r'products', TeaProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]

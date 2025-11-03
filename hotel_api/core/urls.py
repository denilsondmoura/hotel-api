from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HotelViewSet,
    QuartoViewSet,
    ReservaViewSet,
)


router = DefaultRouter()
router.register(r'hoteis', HotelViewSet, basename='hotel')
router.register(r'reservas', ReservaViewSet, basename='reserva')

quartos_list = QuartoViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
quartos_detail = QuartoViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    path('', include(router.urls)),
    path('hoteis/<int:hotel_id>/quartos/', quartos_list, name='hotel-quartos-list-create'),
    path('hoteis/<int:hotel_id>/quartos/<int:pk>/', quartos_detail, name='hotel-quartos-detail'),
]


from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/grafica/', consumers.ChartConsumer.as_asgi()),
]
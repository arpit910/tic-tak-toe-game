from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/asc/pg/<str:game_code>/<str:game_matrix_id>/<str:player_name>/<str:player_type>/', consumers.GameConsumer.as_asgi()),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('game/', views.play, name='game'), 
]

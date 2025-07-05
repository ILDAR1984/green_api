from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GreenAPIViewSet

green_api = GreenAPIViewSet.as_view({
    'post': 'get_settings'
})
get_state = GreenAPIViewSet.as_view({
    'post': 'get_state'
})
send_message = GreenAPIViewSet.as_view({
    'post': 'send_message'
})
send_file = GreenAPIViewSet.as_view({
    'post': 'send_file'
})

urlpatterns = [
    path('get-settings/', green_api, name='get-settings'),
    path('get-state/', get_state, name='get-state'),
    path('send-message/', send_message, name='send-message'),
    path('send-file/', send_file, name='send-file'),
]

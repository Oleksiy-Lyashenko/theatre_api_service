from django.urls import path

from service.views import actor_list

urlpatterns = [
    path("actors/", actor_list, name="actor-list")
]

app_name = "service"

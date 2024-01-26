from django.urls import path, include
from rest_framework import routers

from service.views import (
    ActorModelViewSet,
    GenreModelViewSet,
    PlayModelViewSet,
    PerformanceModelViewSet,
    TheatreHallModelViewSet,
    TicketModelView,
    ReservationModelView
)

# use router for all paths
router = routers.DefaultRouter()
router.register("actors", ActorModelViewSet)
router.register("genres", GenreModelViewSet)
router.register("plays", PlayModelViewSet)
router.register("performances", PerformanceModelViewSet)
router.register("theaters", TheatreHallModelViewSet)
router.register("ticket", TicketModelView)
router.register("reservations", ReservationModelView)


# add router to url
urlpatterns = [
    path("", include(router.urls), )
]

app_name = "service"

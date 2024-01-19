from django.contrib import admin
from service.models import Actor, Genre, Play, Performance, TheatreHall, Ticket, Reservation


admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Play)
admin.site.register(Performance)
admin.site.register(TheatreHall)
admin.site.register(Ticket)
admin.site.register(Reservation)

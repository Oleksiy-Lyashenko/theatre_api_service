from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=63, null=False, unique=True)

    def __str__(self):
        return str(self.name)


class Actor(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=63, null=False, unique=True)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="genres")

    def __str__(self):
        return str(self.title)


class TheatreHall(models.Model):
    name = models.CharField(max_length=63, null=False)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def sum_of_seats(self):
        return int(self.rows * self.seats_in_row)

    def __str__(self):
        return f"{self.name} - {self.sum_of_seats}"


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-show_time"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

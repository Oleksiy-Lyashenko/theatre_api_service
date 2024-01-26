import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=63, null=False, unique=True)

    def __str__(self):
        return str(self.name)


class Actor(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def play_img_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/plays/", filename)


class Play(models.Model):
    title = models.CharField(max_length=63, null=False, unique=True)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="genres")
    image = models.ImageField(null=True, upload_to=play_img_file_path)

    def __str__(self):
        return str(self.title)


class TheatreHall(models.Model): 
    name = models.CharField(max_length=63, null=False, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def num_of_seats(self):
        return int(self.rows * self.seats_in_row)

    def __str__(self):
        return f"{self.name} - {self.num_of_seats}"


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} - {self.theatre_hall.name} - {self.show_time}"

    class Meta:
        ordering = ["-show_time"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reservations", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "performance"], name="unique_ticket_seat_performance")
        ]

    @staticmethod
    def validate_range(row, rows, seat, seats_in_row, error_to_raise):
        if not (1 <= row <= rows):
            raise error_to_raise({
                "rows": f"row must be in range [1, {rows}], not {row}"
            })
        elif not (1 <= seat <= seats_in_row):
            raise error_to_raise({
                "seat": f"seat must be in range [1, {seats_in_row}], not {seat}"
            })

    # Add validation for seats and rows when we choose seat in the performance
    def clean(self):
        Ticket.validate_range(
            self.row,
            self.performance.theatre_hall.rows,
            self.seat,
            self.performance.theatre_hall.seats_in_row,
            ValidationError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)

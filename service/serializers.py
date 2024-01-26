import serializer
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from service.models import Actor, Genre, Play, Performance, TheatreHall, Ticket, Reservation


# Standard implementation serializer
class ActorSerializerStandart(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=63)
    last_name = serializers.CharField(max_length=63)

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


# ModelSerializer has methods create and update, you need only model for serializer
class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor

        # can add different field of model ("first_name",)
        fields = ("id", "first_name", "last_name", "full_name")
        read_only_fields = ("first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres", "image")


class PlayListSerializer(PlaySerializer):
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class PlayDetailSerializer(PlaySerializer):
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "num_of_seats")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title"
    )
    theatre_hall = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
    num_of_seats = serializers.IntegerField(read_only=True, source="theatre_hall.num_of_seats")
    tickets_available = serializers.IntegerField(read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_range(
            attrs["row"],
            attrs["performance"].theatre_hall.rows,
            attrs["seat"],
            attrs["performance"].theatre_hall.seats_in_row,
            serializers.ValidationError
        )

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=["row", "seat", "performance"]
            )
        ]


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayDetailSerializer(many=False)
    theatre_hall = TheatreHallSerializer(many=False)
    tickets = TicketSerializer(many=True)


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(many=False, read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    # can create reservation thorough reservation (read in rest lib writable nested serializer )
    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop('tickets')
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


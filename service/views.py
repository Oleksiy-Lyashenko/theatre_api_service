
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service.models import Actor
from service.serializers import ActorSerializer


# Create your views here.

# @api_view([type of requests]) user rest_framework for beautiful show all these requests
@api_view(["GET"])
def actor_list(request):
    if request.method == "GET":
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)
        # return JsonResponse(serializer.data, status=200, safe=False)
        return Response(serializer.data, status=200)

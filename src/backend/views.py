from django.shortcuts import render
from .serializers import *
from rest_framework import generics


class TeamListCreate(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchListCreate(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ResultListCreate(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


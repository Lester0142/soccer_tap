from django.shortcuts import render
from .serializers import *
from django.http import HttpResponse
import os
from datetime import datetime
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

def download_log_file(request, *args, **kwargs):
    if request.method == "GET":
        # Path to the file you want to serve
        file_path = "zlog_actions.txt"

        # Check if the file exists
        if not os.path.exists(file_path):
            return HttpResponse("File not found", status=404)

        # Open the file in read mode
        with open(file_path, 'r') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            # Add a content-disposition header to tell the browser to download the file
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            response['Content-Disposition'] = f'attachment; filename="log_{current_time}.txt"'
    return response
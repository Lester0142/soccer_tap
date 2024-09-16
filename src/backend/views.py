from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from .utils import *
from django.http import JsonResponse
import json


class TeamListCreate(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchListCreate(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ResultListCreate(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


# Views to interact with users
def insertTeamView(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            data  = json.loads(request.body)
            text_input = data.get('content', None)
            team_preprocess = preprocess_team_text(text_input)
            for team_detail in team_preprocess:
                print(team_detail[2])
                obj, created = Team.objects.update_or_create(
                    name=team_detail[0], 
                    defaults={'date': team_detail[1], 'group': team_detail[2]}
                    )
                log_actions("[insert]: " if created else "[edit]: " + str(team_detail))            
            return JsonResponse({'status':200})
        except Exception as e:
            print(e)
            return JsonResponse({'status':500})


def insertMatchView(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            data  = json.loads(request.body)
            text_input = data.get('content', None)
            match_preprocess = preprocess_match_text(text_input)
            for match_detail in match_preprocess:
                obj, created = Match.objects.update_or_create(
                    team_one=match_detail[0], 
                    team_two=match_detail[1],
                    defaults={'goal_one': match_detail[2], 'goal_two': match_detail[3]}
                    )
                log_actions("[insert]: " if created else "[edit]: " + str(match_detail))            
                return JsonResponse({'status':200})
        except Exception as e:
            print(e)
            return JsonResponse({'status':500})

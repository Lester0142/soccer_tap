from rest_framework import serializers
from .models import *

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'group', 'date')

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'team_one', 'team_two', 'goal_one', 'goal_two')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'name', 'goal', 'date', 'win', 'loss', 'draw', 'point', 'point_alt')

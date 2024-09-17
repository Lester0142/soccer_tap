from django.db import models

# Create your models here.

class Team(models.Model):
    """
    Team Model: holds the team's information
    1. name: team's name
    2. date: date of registration
    3. group: group it belongs to
    """
    name = models.CharField(max_length=100, primary_key=True)
    date = models.DateField()
    group = models.IntegerField()


class Match(models.Model):
    """
    Match Model: holds the match results
    1. team_one: first team one name
    2. team_two: team two name
    3. goals_one: goals scored by team one
    4. goals_two: goals scored by team two
    """
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='t1')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='t2')
    goal_one = models.PositiveIntegerField()
    goal_two = models.PositiveIntegerField()


class Result(models.Model):
    """
    Result Model: evaluated results for the team to determine winners
    1. name: teams' name
    2. goal: goals scored by the team
    3. date: registration date of the team
    4. win: number of wins
    5. draw: number of draws
    6. loss: number of losses
    7. point: points according to first calculation system
    8. point_alt: points according to second calculation system
    """
    name = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal = models.PositiveIntegerField()
    date = models.DateField()
    group = models.IntegerField()
    win = models.PositiveSmallIntegerField()
    draw = models.PositiveSmallIntegerField()
    loss = models.PositiveSmallIntegerField()
    point = models.PositiveSmallIntegerField()
    point_alt = models.PositiveSmallIntegerField()
    rank = models.PositiveSmallIntegerField()
    game = models.PositiveSmallIntegerField()

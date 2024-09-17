from datetime import date, datetime
from .models import *
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
import json

def log_actions(text: str) -> None:
    """
    log actions in text file
    """
    print(text)
    f = open('zlog_actions.txt', 'a+')
    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | " + text + "\n")
    f.close()


def get_post_body(request: any) -> str:
    """"
    extract and return text body of POST request
    TODO: sanitize input
    """
    data  = json.loads(request.body)
    text_input = data.get('content', None)
    return text_input
    

def preprocess_team_text(text_input: str, update: bool=False) -> list[list[str, date, int]]:
    """
    pre-process team insertion text into list of list containing each team details

    E.g.
    input:
        "firstTeam 17/05 2
        secondTeam 07/02 2"
    output:
        [['firstTeam', 17/05/2000, 2], ['secondTeam', 07/02/2000, 2]]
    """
    output = []
    preprocess_text = text_input.split()
    # insertion
    if not update:
        if len(preprocess_text) % 3 != 0:
            raise ValueError("team details length is incorrect.")
        for i in range(0, len(preprocess_text), 3):
            team_name = preprocess_text[i]
            team_date = preprocess_text[i+1].split("/")
            team_grp = preprocess_text[i+2]
            output.append([team_name, 
                        date(day=int(team_date[0]), month=int(team_date[-1]), year=2000),
                        int(team_grp)])
            
    # update/delete
    else:
        if len(preprocess_text) % 4 != 0:
            raise ValueError("team details length for update or del is incorrect.")
        for i in range(0, len(preprocess_text), 4):
            og_name = preprocess_text[i]
            team_name = preprocess_text[i+1]
            team_date = preprocess_text[i+2].split("/")
            team_grp = preprocess_text[i+3]
            output.append([og_name, team_name, 
                        date(day=int(team_date[0]), month=int(team_date[-1]), year=2000),
                        int(team_grp)])
    return output



def preprocess_match_text(text_input: str, update: bool=False) -> list[list[str, str, int, int]]:
    """
    pre-process match insertion text into list of list containing each match details

    E.g.
    input:
        "firstTeam secondTeam 0 3
        thirdTeam fourthTeam 1 1"
    output:
        [['firstTeam', 'secondTeam', 0, 3], ['thirdTeam', 'fourthTeam', 1, 1]]
    """
    output = []
    preprocess_text = text_input.split()
    # insertion
    if not update:
        if len(preprocess_text) % 4 != 0:
            raise ValueError("match details length is incorrect.")
        for i in range(0, len(preprocess_text), 4):
            team_one_name = preprocess_text[i]
            team_two_name = preprocess_text[i+1]
            team_one_goal = preprocess_text[i+2]
            team_two_goal = preprocess_text[i+3]
            output.append([team_one_name, team_two_name, int(team_one_goal), int(team_two_goal)])
    
    # update/delete
    else:
        if len(preprocess_text) % 5 != 0:
            raise ValueError("match details length for update or del is incorrect.")
        for i in range(0, len(preprocess_text), 5):
            id = preprocess_text[i]
            team_one_name = preprocess_text[i+1]
            team_two_name = preprocess_text[i+2]
            team_one_goal = preprocess_text[i+3]
            team_two_goal = preprocess_text[i+4]
            output.append([int(id), team_one_name, team_two_name, int(team_one_goal), int(team_two_goal)])

    return output


def group_ranker():
    """
    Logic to rank the teams by groups in result table.
    
    1. parition by group
    2. order by points desc
    3. order by goals scored desc
    4. order by points alt desc
    5. order by date registered asc
    """

    # update points and update alt points
    results = Result.objects.annotate(
        point_temp = F('win') * 3 + F('draw'),
        point_alt_temp = (F('win') * 5) + (F('draw') * 3) + F('loss')
    )
    for result in results:
        Result.objects.filter(name=result.name).update(point=result.point_temp, point_alt = result.point_alt_temp)

    # update rank
    results = Result.objects.annotate(row_number=Window(
        expression=RowNumber(),
        partition_by=[F('group')],
        order_by=[F('point').desc(), F('goal').desc(), F('point_alt').desc(), F('date').asc()])
        ).order_by('row_number')
    
    for result in results:
        Result.objects.filter(name=result.name).update(rank=result.row_number)


def insert_team_to_result(team_name: models, team_date: date, team_group: int) -> None:
    """
    helper funtion to insert newly added team into result tables
    """
    Result.objects.get_or_create(name=team_name, goal=0, date=team_date, group=team_group, win=0, draw=0, loss=0, point=0, point_alt=0, rank=0)
    group_ranker()
    return

def _win_draw_loss(my_goal: int, their_goal: int) -> None:
    """
    returns win draw or loss
    """
    if my_goal > their_goal:
        return "win"
    elif my_goal < their_goal:
        return "loss"
    else:
        return "draw"

def _update_result(team: models, goal: int, status: str, delete=False) -> None:
    """
    function to update a particular result
    """
    increment = 1
    scored = goal

    if delete:
        scored *= -1
        increment *= -1

    obj = Result.objects.get(name=team)
    obj.goal = obj.goal + scored
    if status == "win":
        obj.win = obj.win + increment
    elif status == "loss":
        obj.loss = obj.loss + increment
    else:
        obj.draw = obj.draw + increment
    obj.save()
    

def update_result_from_match(team_one, team_two, goal_one, goal_two):
    """
    update result after match insertion
    """
    # one - win, two - loss
    if goal_one > goal_two:
        _update_result(team_one, goal_one, "win")
        _update_result(team_two, goal_two, "loss")

    # one - loss, two - win
    elif goal_one < goal_two:
        _update_result(team_one, goal_one, "loss")
        _update_result(team_two, goal_two, "win")
    
    # draw
    else:
        _update_result(team_one, goal_one, "draw")
        _update_result(team_two, goal_two, "draw")

def update_team(team_update_info: list) -> None:
    """
    updates team entry
    """
    # check old team exists
    old_team = Team.objects.get(name=team_update_info[0])
    # create new team
    new_team, created = Team.objects.update_or_create(name=team_update_info[1], 
            defaults={'date': team_update_info[2], 'group':team_update_info[3]})
    # update result
    Result.objects.filter(name=old_team).update(name=new_team,
                                                date=new_team.date,
                                                group=new_team.group)
    # update match if name is changed
    if team_update_info[1] != team_update_info[0]:
        Match.objects.filter(team_one=old_team).update(team_one=new_team)
        Match.objects.filter(team_two=old_team).update(team_two=new_team)

    # delete old team if created
    if created:
        Team.objects.filter(name=team_update_info[0]).delete()

    # update result
    group_ranker()

def update_match(match_update_info: list) -> None:
    """
    updates match entry
    """
    # retrieve old match entry & get the new ones preventing wrong name
    og_match = Match.objects.get(id=match_update_info[0])
    new_team_one = Team.objects.get(name=match_update_info[1])
    new_team_two = Team.objects.get(name=match_update_info[2])
    # undo old match entry on result
    team_one = og_match.team_one
    _update_result(team_one, og_match.goal_one, 
                   _win_draw_loss(og_match.goal_one, og_match.goal_two), delete=True)

    team_two = og_match.team_two
    _update_result(team_two, og_match.goal_two, 
                   _win_draw_loss(og_match.goal_two, og_match.goal_one), delete=True)
    # update result for new match 
    update_result_from_match(new_team_one, new_team_two, match_update_info[3], match_update_info[4])
    # update og_match
    og_match.team_one=new_team_one
    og_match.team_two=new_team_two
    og_match.goal_one=match_update_info[3]
    og_match.goal_two=match_update_info[4]
    og_match.save()
    
    # update result
    group_ranker()


def delete_team(team_delete_info: list) -> None:
    """
    Deletion of team. 
    Matches and result will follow suit due to cascading effect.
    """
    # first remove all the matches played by the team
    old_team = Team.objects.get(name=team_delete_info[0])
    matches = Match.objects.filter(team_one=old_team).all()
    for match in matches:
        delete_match([match.id])

    matches = Match.objects.filter(team_two=old_team).all()
    for match in matches:
        delete_match([match.id])
    
    # delete the result
    Result.objects.filter(name=old_team).delete()

    # delete the team
    Team.objects.filter(name=team_delete_info[0]).delete()

    # update result
    group_ranker()


def delete_match(match_delete_info: list) -> None:
    """
    Deletion of match entry.
    """
    # retrieve old match entry
    og_match = Match.objects.get(id=match_delete_info[0])
    # undo old match entry on result
    team_one = og_match.team_one
    _update_result(team_one, og_match.goal_one, 
                   _win_draw_loss(og_match.goal_one, og_match.goal_two), delete=True)

    team_two = og_match.team_two
    _update_result(team_two, og_match.goal_two, 
                   _win_draw_loss(og_match.goal_two, og_match.goal_one), delete=True)
    # delete match
    Match.objects.filter(id=match_delete_info[0]).delete()
    # update result
    group_ranker()

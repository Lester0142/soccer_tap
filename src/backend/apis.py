from .utils import *
from django.http import JsonResponse
from .models import *


# Apis to interact with users
def insertTeamApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            log_actions("[raw input]: " + text_input)
            team_preprocess = preprocess_team_text(text_input)
            for team_detail in team_preprocess:
                obj, created = Team.objects.get_or_create(
                    name=team_detail[0], 
                    defaults={'date': team_detail[1], 'group': team_detail[2]}
                    )
                if created:
                    log_actions("[insert]: " + str(team_detail))
                    # insert team into result table
                    insert_team_to_result(Team.objects.get(name=team_detail[0]), team_detail[1], team_detail[2])
                else:
                    log_actions("[insert failed, existed]: " + str(team_detail))
            # update result
            group_ranker()       
            return JsonResponse({'status':200})
        except Exception as e:
            log_actions("[insert failed]: " + repr(e))
            return JsonResponse({'status':500})


def insertMatchApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            log_actions("[raw input]: " + text_input)
            match_preprocess = preprocess_match_text(text_input)
            for match_detail in match_preprocess:
                team_one=Team.objects.get(name=match_detail[0]) 
                team_two=Team.objects.get(name=match_detail[1])
                obj, created = Match.objects.get_or_create(
                    team_one=team_one,
                    team_two=team_two,
                    defaults={'goal_one': match_detail[2], 'goal_two': match_detail[3]}
                    )
                if created:
                    log_actions("[insert]: " + str(match_detail))
                    # update results
                    update_result_from_match(team_one, team_two,  match_detail[2], match_detail[3])
                else:
                    log_actions("[insert failed, existed]: " + str(match_detail))
            # update result
            group_ranker()     
            return JsonResponse({'status':200})
        except Exception as e:
            log_actions("[insert failed]: " + repr(e))
            return JsonResponse({'status':500})


def updateTeamApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            log_actions("[raw input]: " + text_input)
            team_preprocess = preprocess_team_text(text_input, update=True)
            # update is supported for individual entries, preprocess list will be of length 1
            update_team(team_preprocess[0])
            log_actions("[update]: " + str(team_preprocess[0]))
            return JsonResponse({'status':200})

        except Exception as e:
            log_actions("[update failed]: " + repr(e))
            return JsonResponse({'status':500})
        

def updateMatchApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            log_actions("[raw input]: " + text_input)
            match_preprocess = preprocess_match_text(text_input, update=True)
            # update is supported for individual entries, preprocess list will be of length 1
            update_match(match_preprocess[0])
            log_actions("[update]: " + str(match_preprocess[0]))
            return JsonResponse({'status':200})

        except Exception as e:
            log_actions("[update failed]: " + repr(e))
            return JsonResponse({'status':500})


def deleteTeamApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            log_actions("[raw input]: " + text_input)
            team_preprocess = preprocess_team_text(text_input, update=True)
            # update is supported for individual entries, preprocess list will be of length 1
            delete_team(team_preprocess[0])
            log_actions("[delete]: " + str(team_preprocess[0]))
            return JsonResponse({'status':200})

        except Exception as e:
            log_actions("[delete failed]: " + repr(e))
            return JsonResponse({'status':500})


def deleteMatchApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            log_actions("[raw input]: " + text_input)
            match_preprocess = preprocess_match_text(text_input, update=True)
            # update is supported for individual entries, preprocess list will be of length 1
            delete_match(match_preprocess[0])
            log_actions("[delete]: " + str(match_preprocess[0]))
            return JsonResponse({'status':200})

        except Exception as e:
            log_actions("[delete failed]: " + repr(e))
            return JsonResponse({'status':500})
        

def deleteAllApi(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            text_input = get_post_body(request)
            if text_input == "delete":
                Match.objects.all().delete()
                Result.objects.all().delete()
                Team.objects.all().delete()
                log_actions("[database wiped]: ========== Empty Database ==========")
                return JsonResponse({'status':200})
            
        except Exception as e:
            log_actions("[delete all failed]: " + repr(e))
            return JsonResponse({'status':500})
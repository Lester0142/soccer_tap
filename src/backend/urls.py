from django.urls import path
from . import views, apis

urlpatterns = [
    path('api/team/', views.TeamListCreate.as_view() ),
    path('api/match/', views.MatchListCreate.as_view() ),
    path('api/result/', views.ResultListCreate.as_view() ),
    path('download/log', views.download_log_file),
    path('insert/team', apis.insertTeamApi),
    path('update/team', apis.updateTeamApi),
    path('delete/team', apis.deleteTeamApi),
    path('insert/match', apis.insertMatchApi),
    path('update/match', apis.updateMatchApi),
    path('delete/match', apis.deleteMatchApi),
    path('delete/all', apis.deleteAllApi),
]
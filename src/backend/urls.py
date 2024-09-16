from django.urls import path
from . import views

urlpatterns = [
    path('api/team/', views.TeamListCreate.as_view() ),
    path('api/match/', views.MatchListCreate.as_view() ),
    path('api/result/', views.ResultListCreate.as_view() ),
    path('insert/team', views.insertTeamView),
    # path('update/team', None),
    # path('delete/team', None),
    path('insert/match', views.insertMatchView),
    # path('update/match', None),
    # path('delete/match', None),
]
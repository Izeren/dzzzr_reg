"""dzzzr_reg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from reg import views


urlpatterns = [
    path('reg/', views.index, name='reg_index'),
    path('team/', views.list_team, name='list_team'),
    path('game_status/', views.list_team, name='game_status_default'),
    path('game_status/<str:pk>', views.game_status, name='game_status'),
    path('tlogin/', views.telegram_login, name='telegram_login'),
    path('add_player/', views.add_player, name='add_player'),
    path('new_game/', views.new_game, name='new_game'),
    path('delete_game/<str:pk>', views.delete_game, name='delete_game'),
    path('delete_user/<str:pk>', views.delete_user, name='delete_user'),
    path('register/<str:pk>', views.register_to_game, name='register_to_game'),
    path('unregister/<str:pk>', views.unregister_from_game, name='unregister_from_game'),
    path('games/', views.list_games, name='list_games'),
    path('export', views.team_export, name='team_export'),
    path('edit/<str:pk>', views.edit_player, name='edit_player'),
]

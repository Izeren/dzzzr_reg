import json
from datetime import datetime

from django import template
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django_tables2 import RequestConfig
from django_tables2.export import TableExport
from django_telegram_login.widgets.constants import SMALL, LARGE, DISABLE_USER_PHOTO
from django_telegram_login.widgets.generator import create_callback_login_widget, create_redirect_login_widget
from django.conf import settings

from reg.forms import NewPlayerForm, NewGameForm
from reg.models import Player, PlayerType, Game, Participation
from reg.tables import HeadQuartersPlayerTable, NonRegisteredPlayerTable, ExportPlayersTable, \
    GamesListTable, RegisteredPlayers, RegisteredFieldPlayerTable


@xframe_options_exempt
def index(request):
    t = template.Engine.get_default().get_template('reg/index.html')
    telegram_login_widget = create_redirect_login_widget(
        settings.TELEGRAM_LOGIN_REDIRECT_URL, settings.TELEGRAM_BOT_NAME, size=LARGE, user_photo=DISABLE_USER_PHOTO
    )
    c = template.Context({'game_name': 'New dozor game', 'telegram_login_widget': telegram_login_widget})
    return HttpResponse(t.render(c))


def telegram_login(request):
    t = template.Engine.get_default().get_template('reg/index.html')
    c = template.Context({'game_name': 'New dozor game'})
    return HttpResponse(t.render(c))


@staff_member_required
def add_player(request):
    if request.method == "POST":
        f = NewPlayerForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('list_team')
    else:
        f = NewPlayerForm()
    return render(request, 'reg/add_player.html', {'form': f})


@staff_member_required
def new_game(request):
    if request.method == "POST":
        f = NewGameForm(request.POST)
        game_exist = len(Game.objects.all().filter(game_name=f.data.get("game_name"))) > 0
        if not game_exist and f.is_valid():
            f.save()
            return redirect('list_games')
    else:
        f = NewGameForm()
    return render(request, 'reg/add_game.html', {'form': f})


@staff_member_required
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return redirect(reverse("list_games"))


@staff_member_required
def delete_user(request, pk):
    player = get_object_or_404(Player, pk=pk)
    player.delete()
    return redirect(reverse("list_team"))


@login_required
def register_to_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    player = get_object_or_404(Player, pk=request.user.id)
    participations = Participation.objects.all().filter(game_id=game, player_id=player)
    if not len(participations):
        participation = Participation(game_id=game, player_id=player)
        participation.save()
    return redirect(reverse("list_team"))


@login_required
def unregister_from_game(request, pk):
    participation = get_object_or_404(Participation, pk=pk)
    participation.delete()
    return redirect(reverse("list_team"))


@login_required
def list_team(request):
    return render(request, 'reg/reg.html', {
        'all': RegisteredPlayers(Player.objects.all()),
    })


@login_required
def game_status(request, pk):
    return render(request, 'reg/game_status.html', {
        'registered_field': RegisteredFieldPlayerTable(Participation.objects.all()
                                                       .filter(game_id=pk)
                                                       .filter(player_id__role=PlayerType.FIELD.name)),
        'registered_headquarters': HeadQuartersPlayerTable(Participation.objects.all()
                                                           .filter(game_id=pk)
                                                           .filter(player_id__role=PlayerType.HEADQUARTERS.name)),
        'reserve': NonRegisteredPlayerTable(Participation.objects.all()
                                            .filter(game_id=pk)
                                            .filter(player_id__role=PlayerType.NOT_PLAYING.name)),
    })


@login_required
def list_games(request):
    return render(request, 'reg/games.html', {
        'games': GamesListTable(Game.objects.all()),
    })


@login_required
def edit_player(request, pk):
    player = get_object_or_404(Player, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = NewPlayerForm(request.POST, instance=player)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            f.save()
            return redirect(reverse('list_team'))

    # if request is GET the show unbound form to the user, along with data
    elif player.user_id == request.user:
        f = NewPlayerForm(instance=player)
    else:
        return redirect(reverse("list_team"))

    return render(request, 'reg/edit_player.html', {'form': f, 'post': player})


@login_required
def team_export(request):
    table = ExportPlayersTable(Player.objects.all())

    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, "reg/export_players.html", {
        "table": table
    })

# class TeamView(MultiTableMixin, TemplateView):
#     template_name = 'reg/reg.html'
#     tables = [
#         FieldPlayerTable(Player.objects.all().filter(role=PlayerType.FIELD.name)),
#         HeadQuartersPlayerTable(Player.objects.all().filter(role=PlayerType.HEADQUARTERS.name)),
#         NonRegisteredPlayerTable(Player.objects.all().filter(role=PlayerType.NOT_PLAYING.name))
#     ]

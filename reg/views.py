import json
from datetime import datetime

from django import template
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django_tables2 import RequestConfig
from django_tables2.export import TableExport

from reg.forms import NewPlayerForm
from reg.models import Player, PlayerType
from reg.tables import FieldPlayerTable, HeadQuartersPlayerTable, NonRegisteredPlayerTable, ExportPlayersTable


def index(request):
    t = template.Engine.get_default().get_template('reg/index.html')
    c = template.Context({'game_name': 'New dozor game'})
    return HttpResponse(t.render(c))


def add_player(request):
    if request.method == "POST":
        f = NewPlayerForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('list_team')
    else:
        f = NewPlayerForm()
    return render(request, 'reg/add_player.html', {'form': f})


def list_team(request):
    return render(request, 'reg/reg.html', {
        'field': FieldPlayerTable(Player.objects.all().filter(role=PlayerType.FIELD.name)),
        'headquarters': HeadQuartersPlayerTable(Player.objects.all().filter(role=PlayerType.HEADQUARTERS.name)),
        'non_registered': NonRegisteredPlayerTable(Player.objects.all().filter(role=PlayerType.NOT_PLAYING.name))
    })


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
    else:
        f = NewPlayerForm(instance=player)

    return render(request, 'reg/edit_player.html', {'form': f, 'post': player})


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

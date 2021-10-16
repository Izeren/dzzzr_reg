from django.utils.html import format_html
from django_tables2 import tables, Column

from reg import REMOVE_SYMBOL
from reg.models import Player, Game, Participation


class EditColumn(Column):
    def render(self, value):
        return format_html("<form action=/reg/edit/{}> <input type=submit value='edit player'> </form>", value)


class RegisterToGame(Column):
    def render(self, value):
        return format_html("<a href=/reg/register/{}>Зарегистрироваться на игру</a>", value)


class UnregisterFromGame(Column):
    def render(self, value):
        return format_html("<a href=/reg/unregister/{}><span>&#10060;</span></a>", value)


class DeleteGame(Column):
    def render(self, value):
        return format_html("<a href=/reg/delete_game/{}><span>&#10060;</span></a>", value)


class DeleteUser(Column):
    def render(self, value):
        return format_html("<a href=/reg/delete_user/{}><span>&#10060;</span></a>", value)


class GameStatus(Column):
    def render(self, value):
        return format_html("<a href=/reg/game_status/{}>Обзор</a>", value)


class RegisteredFieldPlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap-responsive.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("player_id.user_id", "player_id.name", "player_id.nick", "player_id.car", "player_id.driver",
                  "player_id.danger_code", "player_id.radio", "player_id.phone_charger", "player_id.flashlight",
                  "player_id.headlight", "player_id.uv_light", "player_id.notes",)
    edit = EditColumn(verbose_name="", accessor="player_id.player_id")
    unregister = UnregisterFromGame(verbose_name="", accessor="record_id")


class RegisteredPlayers(tables.Table):
    class Meta:
        model = Player
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("user_id", "name", "nick", "role", "car", "driver", "danger_code", "radio", "phone_charger",
                  "flashlight", "headlight", "uv_light", "notes",)
    edit = EditColumn(verbose_name="", accessor="pk")
    delete = DeleteUser(verbose_name="", accessor="pk")


class GamesListTable(tables.Table):
    class Meta:
        model = Game
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("game_id", "game_name",)
    status = GameStatus(verbose_name="Состав игроков", accessor="game_id")
    register = RegisterToGame(verbose_name="Зарегистрироваться на игру", accessor="game_id")
    delete = DeleteGame(verbose_name="Удалить игру", accessor="game_id")


class HeadQuartersPlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("player_id.name", "player_id.nick", "player_id.laptop", "player_id.notes",)
    edit = EditColumn(verbose_name="", accessor="player_id.player_id")
    unregister = UnregisterFromGame(verbose_name="", accessor="record_id")


class NonRegisteredPlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("player_id.name", "player_id.nick", "player_id.car", "player_id.driver", "player_id.danger_code",
                  "player_id.radio", "player_id.phone_charger", "player_id.flashlight", "player_id.headlight",
                  "player_id.uv_light", "player_id.laptop", "player_id.notes",)
    edit = EditColumn(verbose_name="", accessor="player_id.player_id")
    unregister = UnregisterFromGame(verbose_name="", accessor="record_id")


class ExportPlayersTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("name", "nick", "phone", "car", "driver", "danger_code", "radio", "phone_charger",
                  "flashlight", "headlight", "uv_light", "laptop", "notes",)


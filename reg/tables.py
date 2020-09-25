from django.utils.html import format_html
from django_tables2 import tables, Column

from reg.models import Player


class EditColumn(Column):
    def render(self, value):
        return format_html("<a href=/reg/edit/{}>Изменить анкету</a>", value)


class FieldPlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap-responsive.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("name", "nick", "phone", "car", "driver", "danger_code", "radio", "phone_charger",
                  "flashlight", "headlight", "uv_light", "notes",)
    edit = EditColumn(verbose_name="Редактировать", accessor="pk")


class HeadQuartersPlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("name", "nick", "phone", "laptop", "notes",)
    edit = EditColumn(verbose_name="Редактировать", accessor="pk")


class NonRegisteredPlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("name", "nick", "phone", "car", "driver", "danger_code", "radio", "phone_charger",
                  "flashlight", "headlight", "uv_light", "laptop", "notes",)

    edit = EditColumn(verbose_name="Редактировать", accessor="pk")


class ExportPlayersTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        fields = ("name", "nick", "phone", "car", "driver", "danger_code", "radio", "phone_charger",
                  "flashlight", "headlight", "uv_light", "laptop", "notes",)


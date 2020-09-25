from django import forms

from reg.models import Player


class NewPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = "__all__"

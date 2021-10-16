from django import forms

from reg.models import Player, Game


class NewPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = "__all__"


class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"

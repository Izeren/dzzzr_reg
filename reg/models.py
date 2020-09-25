from enum import Enum

from django.db import models

from reg import MAX_NAME_LENGTH, MAX_PLAYER_NOTES_LENGTH, MAX_PHONE_LENGTH, COMMENT_HELP_TEXT, NAME_REF, ROLE_REF, \
    DANGER_CODE_REF, NOTES_REF, PHONE_REF, FLASHLIGHT_REF, HEADLIGHT_REF, UV_REF, RADIO_REF, LAPTOP_REF, \
    PHONE_HELP_TEXT, NICK_REF, DRIVER_REF, CAR_REF, CHARGER_REF, LEVEL_REF


class ChoiceableEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)

    @classmethod
    def get_max_name_length(cls):
        return max([max(len(choice.name), len(choice.value)) for choice in cls])


class PlayerType(ChoiceableEnum):
    NOT_PLAYING = "Не играю"
    FIELD = "Полевой"
    HEADQUARTERS = "Штабной"


class CarColor(ChoiceableEnum):
    NO_CAR = "Без экипажа"
    RED = "Красный"
    YELLOW = "Желтый"
    GREEN = "Зеленый"
    BLUE = "Синий"
    VIOLET = "Фиолетовый"
    WHITE = "Белый"
    BLACK = "Черный"


class Level(ChoiceableEnum):
    NOVICE = "Новичок(0)"
    MODERATE = "Посвященный(1)"
    EXPERT = "Эксперт(2)"


class LabelDangerCode(ChoiceableEnum):
    OMG = "omg, что это?"
    NO_DANGER = "Я штабик, у меня лапки"
    BASIC = "1"
    BASIC_EXTRA = "1+"
    MEDIUM = "2"
    MEDIUM_EXTRA = "2+"
    HARD = "3"
    HARD_EXTRA = "3+"


class DriverType(ChoiceableEnum):
    NO_DRIVER = "Не в этот раз"
    CAR_ONWER = "на своей"
    CARSHARING = "каршеринг"


class Player(models.Model):
    name = models.CharField(verbose_name=NAME_REF, max_length=MAX_NAME_LENGTH)
    nick = models.CharField(verbose_name=NICK_REF, max_length=MAX_NAME_LENGTH, unique=True)
    role = models.CharField(verbose_name=ROLE_REF, max_length=PlayerType.get_max_name_length(),
                            choices=PlayerType.choices(), default=PlayerType.NOT_PLAYING)
    danger_code = models.CharField(verbose_name=DANGER_CODE_REF, max_length=LabelDangerCode.get_max_name_length(),
                                   choices=LabelDangerCode.choices(), default=LabelDangerCode.OMG)
    notes = models.CharField(verbose_name=NOTES_REF, max_length=MAX_PLAYER_NOTES_LENGTH, help_text=COMMENT_HELP_TEXT,
                             null=True, blank=True)
    phone = models.CharField(verbose_name=PHONE_REF, max_length=MAX_PHONE_LENGTH, help_text=PHONE_HELP_TEXT)
    flashlight = models.BooleanField(verbose_name=FLASHLIGHT_REF, default=False)
    headlight = models.BooleanField(verbose_name=HEADLIGHT_REF, default=False)
    uv_light = models.BooleanField(verbose_name=UV_REF, default=False)
    radio = models.BooleanField(verbose_name=RADIO_REF, default=False)
    laptop = models.BooleanField(verbose_name=LAPTOP_REF, default=False)
    driver = models.CharField(verbose_name=DRIVER_REF, max_length=DriverType.get_max_name_length(),
                              choices=DriverType.choices(), default=DriverType.NO_DRIVER)
    car = models.CharField(verbose_name=CAR_REF, max_length=CarColor.get_max_name_length(),
                           choices=CarColor.choices(), default=CarColor.NO_CAR)
    phone_charger = models.BooleanField(verbose_name=CHARGER_REF, default=False)
    level = models.CharField(verbose_name=LEVEL_REF, max_length=Level.get_max_name_length(),
                             choices=Level.choices(), default=Level.NOVICE)





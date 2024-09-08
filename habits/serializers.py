from rest_framework import serializers

from habits.models import Habits
from habits.validators import (
    HabitsDurationValidator,
    validate_related_or_prize,
    validate_related_is_nice,
    validate_nice_navent_prize_and_related,
    periodicy_is_often_then_once_a_week,
    HabitsPeriodicValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    validators = [
        HabitsDurationValidator(field="duration"),
        HabitsPeriodicValidator(field="periodicity"),
    ]

    # при создании и редаткировании полей отрабатывает метод валидации полей
    # на вход он забирает модель, оттуда по имени забирает поле, далее применяется правило валидации
    class Meta:
        model = Habits
        fields = "__all__"
        # validators = [HabitsValidator]

    def validate(self, data):
        """
        У приятной привычки не может быть вознаграждения или связанной привычки. Исключить одновременный выбор
        связанной привычки и указания вознаграждения. В модели не должно быть заполнено одновременно и поле
        вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.

        Привычка должна быть исполнена не реже чем раз в 7 дней.
        """

        message = validate_related_or_prize(data) + validate_related_is_nice(data)
        message += validate_nice_navent_prize_and_related(
            data
        ) + periodicy_is_often_then_once_a_week(data)

        if message:
            raise serializers.ValidationError(message)

        return data

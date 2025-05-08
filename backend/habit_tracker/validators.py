from habit_tracker import exceptions


class SimultaneousSelected:
    """
    Исключить одновременный выбор связанной привычки
    и указания вознаграждения.
    """

    requires_context = True

    def __call__(self, value, serializer_field):
        if value.get("related") and value.get("reward"):
            raise exceptions.UnprocessableEntityError(
                dict(
                    error="ValidationError",
                    serial="одновременный выбор 'related' и 'reward'.",
                )
            )


class TimeValid:
    """
    Время выполнения должно быть не больше 120 секунд.
    """

    requires_context = True

    def __call__(self, value, serializer_field):
        if value.get("time") > 120 or value.get("time") <= 0:
            raise exceptions.UnprocessableEntityError(
                dict(
                    error="ValidationError",
                    serial="должно быть в пределах 1-120 секунд.",
                )
            )


class SignNice:
    """
    В связанные привычки могут попадать только привычки
    с признаком приятной привычки.
    """

    requires_context = True

    def __call__(self, value, serializer_field):
        related = value.get("related")
        if related:
            if related.nice:
                raise exceptions.UnprocessableEntityError(
                    dict(
                        error="ValidationError",
                        serial="Связанная привычка не 'приятная'",
                    )
                )


class HabitNiceValid:
    """
    У приятной привычки не может быть
    вознаграждения или связанной привычки.
    """

    requires_context = True

    def __call__(self, value, serializer_field):
        if value.get("nice"):
            if value.get("related", False) or value.get("reward", False):
                raise exceptions.UnprocessableEntityError(
                    dict(
                        error="ValidationError",
                        serial="У 'приятной' не должно быть "
                               "связанной или вознаграждения",
                    )
                )


class PeriodValid:
    """
    Нельзя выполнять привычку реже,
    чем 1 раз в 7 дней.
    """

    requires_context = True

    def __call__(self, value, serializer_field):
        """if value.get("period") > 7 or value.get("period") <= 0:
        raise exceptions.UnprocessableEntityError(
            dict(error="ValidationError",
                 serial="period - должно быть в пределах 1-120 секунд.")
        )"""

        day_of_week = value.get("period", "1,2,3,4,5,6,0").split(",")
        for day in day_of_week:
            if not day.isdigit():
                raise exceptions.UnprocessableEntityError(
                    dict(
                        error="ValidationError",
                        serial="period должно быть в пределе '1,2,3,4,5,6,0'.",
                    )
                )
            if int(day) > 6:
                raise exceptions.UnprocessableEntityError(
                    dict(
                        error="ValidationError",
                        serial="period должно быть в пределе '1,2,3,4,5,6,0'.",
                    )
                )

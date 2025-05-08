from django.db import models

from users.models import CustomUser


# Create your models here.


class Habit(models.Model):
    user = models.ForeignKey(
        CustomUser,
        null=False,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="юзер создавший привычку",
    )
    place = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True,
        verbose_name="место выполнения привычки",
        help_text="место, в котором необходимо выполнять привычку",
    )

    time_action = models.TimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name="время выполнения привычки",
        help_text="время, когда необходимо выполнять привычку",
    )
    period = models.CharField(
        max_length=50,
        default="1,2,3,4,5,6,7",
        blank=True,
        verbose_name="день недели, когда необходимо выполнять привычку",
        help_text="дни недели через запятую 1,2,3,4,5,6,7",
    )
    action = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True,
        verbose_name="действие-привычка",
        help_text="действие, которое представляет собой привычка.",
    )
    nice = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки")
    related = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="to_related",
        verbose_name="ссылка на полезную привычку",
    )
    reward = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True,
        verbose_name="чем пользователь должен себя вознаградить",
        help_text="вознаграждение",
    )
    time = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="время на выполнение привычки в секундах"
    )
    public = models.BooleanField(
        default=False,
        verbose_name="привычки можно публиковать в общий доступ"
    )

    def __str__(self):
        return self.action

    def __repr__(self):
        return f"{self.pk} {self.action}"

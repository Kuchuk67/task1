from config.celery import app
from habit_tracker.models import Habit
from telegram_bot.services import send_telegram_message

@app.task()
def task_habit(id_habit):
    print("++++++++++++", id_habit)
    id_habit = int(id_habit)
    habit = Habit.objects.get(pk=id_habit)
    message = (
        f"Напоминание: Выполните привычку '{habit.action}'"
        f" в локации '{habit.place}' "
        f"время выполнения: {habit.time}. "
        f"Вознаграждение: "
        f"{habit.reward if habit.reward else habit.related.action}."
    )
    send_telegram_message(message, habit.user.chat_id_telegram)
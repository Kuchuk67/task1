from datetime import datetime

from channels.db import database_sync_to_async
from django.core.management.base import BaseCommand
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes)
from habit_tracker.models import Habit
from users.models import CustomUser
from config.settings import BOT_TOKEN

class Command(BaseCommand):

    def button_bot(self, update):

        keyboard = [
            [
                InlineKeyboardButton("Задачи на сегодня", callback_data="1"),
                InlineKeyboardButton("Задачи на завтра", callback_data="2"),
            ],
            [InlineKeyboardButton("10 возможных задач", callback_data="3")],
        ]
        return InlineKeyboardMarkup(keyboard)

    @database_sync_to_async
    def add_id_chat(self, update):
        user = CustomUser.objects.get(
            nick_telegram=update.effective_chat.username)
        user.chat_id_telegram = update.effective_chat.id
        user.save()
        return user

    @database_sync_to_async
    def habits_now(self, update):
        habits = Habit.objects.filter(
            user__chat_id_telegram=update.effective_chat.id,
            nice=False,
        )
        dw = datetime.now().isoweekday()
        if dw == 7:
            dw = 0
        habit_list = "На сегодня запланировано:\n"
        for habit in habits:
            # отсеиваем по дням недели
            if str(dw) in habit.period:
                habit_list += f"{habit.time_action} -  {habit.action} \n"
        return habit_list

    @database_sync_to_async
    def habits_tomorrow(self, update):
        habits = Habit.objects.filter(
            user__chat_id_telegram=update.effective_chat.id,
            nice=False,
        )
        dw = datetime.now().isoweekday() + 1
        if dw == 8:
            dw = 1
        if dw == 7:
            dw = 0
        habit_list = "На завтра запланировано:\n"
        for habit in habits:
            # отсеиваем по дням недели
            if str(dw) in habit.period:
                habit_list += f"{habit.time_action} -  {habit.action} \n"
        return habit_list

    @database_sync_to_async
    def habits_top(self, update):
        """ Вывести 10 последних публичных задач"""
        habits = Habit.objects.filter(public=True).order_by("-id")
        habit_list = "10 новых публичных привычек: :\n"
        i = 1
        for habit in habits:
            habit_list += f"{i}.  {habit.action} \n"
            i += 1
        return habit_list

    def handle(self, *args, **kwargs):
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Привет! Я бот трекер-сарвиса 'Атомарные привычки'!",
            )
            # Тут надо найти в БД пользователя с ником телеграма
            try:
                await self.add_id_chat(update)
            except Exception:
                # НЕ найдено - пишем что надо зарегится на сервисе
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Не найден такой ник. Вам надо зарегится на сервисе "
                    "и указать в профиле свой ник в телеге",
                    # reply_markup=keyboard
                )
            else:
                # найдено - записываем туда chat_id и пишем - ок
                await update.message.reply_text(
                    "Пожалуйста, выберите:",
                    reply_markup=self.button_bot(update)
                )

        async def button(update, _):
            query = update.callback_query
            variant = query.data
            # `CallbackQueries` требует ответа, даже если
            # уведомление для пользователя не требуется, в противном
            #  случае у некоторых клиентов могут возникнуть проблемы.
            # смотри https://core.telegram.org/bots/api#callbackquery.
            await query.answer()

            # редактируем сообщение, тем самым кнопки
            # в чате заменятся на этот ответ.
            habit_list = ""
            # Обработка - задачи на сегодня
            if variant == "1":
                habit_list = await self.habits_now(update)
            # Обработка - задачи на завтра
            if variant == "2":
                habit_list = await self.habits_tomorrow(update)
            # Обработка - 10 публичных задач
            if variant == "3":
                habit_list = await self.habits_top(update)

            await query.edit_message_text(text=f"{habit_list}")

        # Токен телеграма
        application = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .build()
        )
        # Добавить обработчик /start
        start_handler = CommandHandler("start", start)
        application.add_handler(start_handler)
        # Добавить обработчик  нажатия кнопки
        application.add_handler(CallbackQueryHandler(button))
        # Зацикливание
        application.run_polling()

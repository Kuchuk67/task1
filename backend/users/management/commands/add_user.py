from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # CustomUser.objects.all().delete()

        # Создаем суперпользователя
        user = CustomUser.objects.get(
            email="admin@mail.ru",
        )
        if not user:
            user = CustomUser.objects.create(
                email="admin@mail.ru",
            )
            user.set_password("12345")
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()

        """user = CustomUser.objects.create(
            email="user@mail.ru",
        )
        user.set_password("12345")
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()"""

        # Создаем новую группу
        # new_group, created = Group.objects.get_or_create(name="Модератор")

        # print("Создаем новую группу", new_group, created)

        # ct = ContentType.objects.get_for_model(CustomUser)
        #
        # permission = Permission.objects.create(
        #    codename="can_moderation_users",
        #    name="Модерировать пользователей",
        #    content_type=ct,
        # )
        # new_group.permissions.add(permission)
        # ct = ContentType.objects.get_for_model(Task)
        # permission = Permission.objects.create(
        #    codename="can_moderation_mailing",
        #    name="Модерировать рассылки",
        #    content_type=ct,
        # )
        # new_group.permissions.add(permission)
        # print("Подключили пермишены")

        """CustomUser.objects.get_or_create(
                pk=1,
                username='admin',
                email='kuchukov.s@mail.ru',
                password='12345',
                is_staff=True,
                is_superuser=True,
            )"""

    """
        CustomUser.objects.get_or_create(
            pk=2,
            username='Модератор Василий',
            email='moder@mail.ru',
            password='12345',
        )
        CustomUser.objects.get_or_create(
            pk=3,
            username='User',
            email='user@mail.ru',
            password='12345',
        )"""

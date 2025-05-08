from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from habit_tracker.models import Habit
from habit_tracker.serializer import HabitSerializer
from rest_framework.permissions import IsAuthenticated


class HabitViewsSet(ModelViewSet):
    # pagination_class = EducationPagination
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the object the view is displaying
        only for current user.
        """
        return Habit.objects.filter(user=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        request.data["user"] = self.request.user.pk
        return super().create(request, *args, **kwargs)


class HabitListViews(ListAPIView):
    # pagination_class = EducationPagination
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(public=True)
    permission_classes = [IsAuthenticated]

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from api.permissions import IsTrainer
from api.serializers import ExerciseSerializer, DaySerializer, PlanSerializer, UserSerializer
from vg.models import Exercise, Day, Plan

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExerciseList(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticated, IsTrainer, )

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsTrainer,)


class DayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class DayList(generics.ListCreateAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class PlanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanList(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

@api_view(['POST', 'DELETE'])
def add_remove_day_from_plan(request, plan_pk):
    plan = get_object_or_404(Plan, pk=plan_pk)
    content = PlanSerializer(plan)
    day = get_object_or_404(Day, pk=request.data['day'])

    if request.method == 'POST':
        if day in plan.days.all():
            return Response(content.data, status=status.HTTP_304_NOT_MODIFIED)
        plan.days.add(day)
        plan.save()
        content = PlanSerializer(plan)
        return Response(content.data)

    elif request.method == 'DELETE':
        if not day in plan.days.all():
            return Response(content.data, status=status.HTTP_406_NOT_ACCEPTABLE)

        plan.days.remove(day)
        plan.save()
        content = PlanSerializer(plan)
        return Response(content.data)

@api_view(['POST', 'DELETE'])
def add_remove_exercise_from_day(request, day_pk):
    day = get_object_or_404(Day, pk=day_pk)
    content = DaySerializer(day)
    exercise = get_object_or_404(Exercise, pk=request.data['exercise'])

    if request.method == 'POST':
        if exercise in day.exercises.all():
            return Response(content.data, status=status.HTTP_304_NOT_MODIFIED)

        day.exercises.add(exercise)
        day.save()
        content = DaySerializer(day)
        return Response(content.data)

    elif request.method == 'DELETE':
        if not exercise in day.exercises.all():
            return Response(content.data, status=status.HTTP_406_NOT_ACCEPTABLE)

        day.exercises.remove(exercise)
        day.save()
        content = DaySerializer(day)
        return Response(content.data)

@api_view(['POST', 'DELETE'])
def add_remove_user_from_plan(request, plan_pk):
    plan = get_object_or_404(Plan, pk=plan_pk)
    content = PlanSerializer(plan)
    user = get_object_or_404(User, pk=request.data['user'])

    if request.method == 'POST':
        if user in plan.assigned_to.all():
            return Response(content.data, status=status.HTTP_304_NOT_MODIFIED)
        plan.assigned_to.add(user)
        plan.save()
        content = PlanSerializer(plan)
        return Response(content.data)

    elif request.method == 'DELETE':
        if not user in plan.days.all():
            return Response(content.data, status=status.HTTP_406_NOT_ACCEPTABLE)

        plan.assigned_to.remove(user)
        plan.save()
        content = PlanSerializer(plan)
        return Response(content.data)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView

from vg.models import Exercise, Day, Profile, Plan


class BaseTrainerView(LoginRequiredMixin, UserPassesTestMixin):
    """Base class to give access only to trainers to update training plans, etc.
    """
    def test_func(self):
        return self.request.user.profile.type_user == Profile.TRAINER


class ExerciseList(BaseTrainerView, ListView):
    model = Exercise
    context_object_name = 'exercises'


class ExerciseCreate(BaseTrainerView, CreateView):
    model = Exercise
    fields = ['title', 'description']


class ExerciseUpdate(BaseTrainerView, UpdateView):
    model = Exercise
    fields = ['title', 'description']

    def form_valid(self, form):
        now = timezone.now()
        exercise = form.save(commit=False)
        exercise.updated_by = self.request.user
        exercise.updated_date = now
        exercise.save()
        messages.success(self.request, 'Exercise updated')
        return redirect('exercise', pk=exercise.pk)


class DayList(BaseTrainerView, ListView):
    model = Day
    context_object_name = 'days'


class DayCreate(BaseTrainerView, CreateView):
    model = Day
    fields = ['exercises']


class DayUpdate(BaseTrainerView, UpdateView):
    model = Day
    fields = ['exercises']
    context_object_name = 'day'

    def form_valid(self, form):
        day = form.save(commit=False)
        day.updated_date = timezone.now()
        day.updated_by = self.request.user
        day.save()
        form.save_m2m()
        messages.success(self.request, 'Day Updated')
        return redirect('day', pk=day.pk)


class PlanList(BaseTrainerView, ListView):
    model = Plan
    context_object_name = 'plans'

class PlanCreate(BaseTrainerView, CreateView):
    model = Plan
    fields = ['name', 'days']

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.created_by = self.request.user
        plan.save()
        form.save_m2m()
        return redirect('plan', pk=plan.pk)


class PlanUpdate(BaseTrainerView, UpdateView):
    model = Plan
    fields = ['name', 'days']

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.updated_date = timezone.now()
        plan.updated_by = self.request.user
        plan.save()
        form.save_m2m()
        return redirect('plan', pk=plan.pk)


class AssignPlan(BaseTrainerView, UpdateView):
    model = Plan
    fields = ['assigned_to']
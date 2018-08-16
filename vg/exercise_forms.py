from django.forms import ModelForm

from vg.models import Exercise, Day, Plan


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['description', 'title']


class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = ['exercises']


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'days']
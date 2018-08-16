from django.contrib.auth.models import User
from rest_framework import serializers

from vg.models import Exercise, Day, Plan, Profile


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(read_only=True, many=True)
    class Meta:
        model = Day
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    days = DaySerializer(read_only=True, many=True)
    class Meta:
        model = Plan
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, many=False)
    class Meta:
        model = User
        fields = '__all__'
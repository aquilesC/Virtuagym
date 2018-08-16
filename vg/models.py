import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.utils import timezone


class Profile(models.Model):
    """Extendable model for users. It allows to define roles, etc. without tampering with Django auth models.
    """
    TRAINER, CLIENT = 0, 1
    type_user_choices = (
        (TRAINER, 'Trainer'),
        (CLIENT, 'Client'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, default='', verbose_name='Biography')
    type_user = models.IntegerField(choices=type_user_choices, default=TRAINER)

    def __str__(self):
        return 'Profile for {}'.format(self.user.username)

    def __repr__(self):
        return '<Profile: {}>'.format(self.user.username)


class Note(models.Model):
    """Notes attached to a user. To keep track of what trainers think.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500, blank=False)


class Exercise(models.Model):
    """Definition of an exercise. It is the base unit for a workout plan.
    """
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='exercise_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, related_name='exercise_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, default='')
    title = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/exercise/{}'.format(self.id)


class Day(models.Model):
    """A day consists of several exercises. A collection of days make a workout plan.
    """
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='day_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='day_updated_by', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)

    def get_absolute_url(self):
        return '/day/{}'.format(self.pk)

    def __str__(self):
        name = ['{}'.format(ex.title) for ex in self.exercises.all()]
        return ' '.join(name)


class Plan(models.Model):
    """A plan is a collection of days, each consisting of several exercises. Every time a user is assigned to a plan, or a plan
    is updated, an e-mail will be sent to the user to let them know of the changes.
    """
    name = models.CharField(max_length=30, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='plan_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='plan_updated_by', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    days = models.ManyToManyField(Day)
    assigned_to = models.ManyToManyField(User, related_name='assigned_to', blank=True)

    @property
    def trainees(self):
        trainees = [u.username for u in self.assigned_to.all()]
        return ' '.join(trainees)

    def get_absolute_url(self):
        return '/plan/{}'.format(self.pk)

    def __str__(self):
        return self.name


class PlanUpdates(models.Model):
    """Keeps track of the messages sent to users in order to avoid contacting them more than once per 24hours. For
    example, updating an exercise present in different days would trigger several plan updates.
    """
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=False, related_name='plan')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='updated_by')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='sent_to')



def create_profile(sender, **kwargs):
    """Guarantees that every time a user is created there is a corresponding profile associated.
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()


def exercise_update(sender, **kwargs):
    """If an exercise is updated, it propagates to the days as well.
    """
    exercise = kwargs['instance']
    for day in exercise.day_set.all():
        day.updated_by = exercise.updated_by
        day.updated_date = exercise.updated_date
        day.save()


def day_update(sender, **kwargs):
    """If a day is updated, the changes are propagated to the plans.
    """
    day = kwargs['instance']
    for plan in day.plan_set.all():
        plan.updated_date = day.updated_date
        plan.updated_by = day.updated_by
        plan.save()


def plan_update(sender, **kwargs):
    """If a plan is updated, an e-mail will be sent to all the users that were assigned to that plan.
    """
    plan = kwargs['instance']
    sbj = 'Training plan updated'
    msg = 'Your training plan {} has been updated.'.format(plan)
    from_email = 'virtualgym@virtualgym.com'
    for user in plan.assigned_to.all():
        recent_updates = PlanUpdates.objects.filter(sent_to=user, updated_date__gt=timezone.now()-datetime.timedelta(days=1))
        if len(recent_updates) == 0:
            update = PlanUpdates(sent_to=user, plan=plan, updated_by=plan.updated_by)
            update.save()
            send_mail(sbj, msg, from_email, ['{} <{}>'.format(user.username,user.email)])



post_save.connect(create_profile, sender=User)
post_save.connect(exercise_update, sender=Exercise)
post_save.connect(day_update, sender=Day)
post_save.connect(plan_update, sender=Plan)
m2m_changed.connect(plan_update, sender=Plan)
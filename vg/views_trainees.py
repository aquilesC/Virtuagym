from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from vg.models import Plan


class PlanList(LoginRequiredMixin, ListView):
    model = Plan
    context_object_name = 'plans'

    def get_queryset(self):
        plans = Plan.objects.filter(assigned_to=self.request.user)
        return plans
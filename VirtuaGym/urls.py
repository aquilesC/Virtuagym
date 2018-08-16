"""VirtuaGym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from vg.auth_views import LoginView, SignUpView, index, SignUpSuccess
from vg.views_trainer import ExerciseCreate, ExerciseUpdate, DayCreate, DayUpdate, PlanUpdate, PlanCreate, AssignPlan, \
    ExerciseList, DayList, PlanList

from vg import views_trainees

from api.urls import urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('signup_success', SignUpSuccess.as_view(), name='signup_success'),
    path('exercise', ExerciseList.as_view(), name='exercises'),
    path('exercise/create', ExerciseCreate.as_view(), name='exercise_create'),
    path('exercise/<int:pk>', ExerciseUpdate.as_view(), name='exercise'),
    path('day', DayList.as_view(), name='days'),
    path('day/create', DayCreate.as_view(), name='day_create'),
    path('day/<int:pk>', DayUpdate.as_view(), name='day'),
    path('plan', PlanList.as_view(), name='plans'),
    path('plan/create', PlanCreate.as_view(), name='plan_create'),
    path('plan/<int:pk>', PlanUpdate.as_view(), name='plan'),
    path('plan/<int:pk>/assign', AssignPlan.as_view(), name='assign_plan'),
    path('u/plan', views_trainees.PlanList.as_view(), name='plan_list_trainee'),
    path('api/', include('api.urls'), name='api'),
    path('logout', LogoutView.as_view(), name='logout'),
]

from django.urls import path

from .views import (ExerciseList,
                    ExerciseDetail,
                    PlanList,
                    PlanDetail,
                    DayDetail,
                    DayList,
                    add_remove_day_from_plan,
                    add_remove_exercise_from_day,
                    add_remove_user_from_plan,
                    UserDetail,
                    UserList,
                    )


urlpatterns = [
    path('exercise', ExerciseList.as_view(), name='exercise_list'),
    path('exercise/<pk>', ExerciseDetail.as_view(), name='exercise_detail'),
    path('plan', PlanList.as_view(), name='plan_list'),
    path('plan/<pk>', PlanDetail.as_view(), name='plan_detail'),
    path('day', DayList.as_view(), name='day_list'),
    path('day/<pk>', DayDetail.as_view(), name='day_detail'),
    path('plan/<plan_pk>/add_day', add_remove_day_from_plan, name='add_day_to_plan'),
    path('plan/<plan_pk>/add_user', add_remove_user_from_plan, name='add_user_to_plan'),
    path('day/<day_pk>/add_exercise', add_remove_exercise_from_day, name='add_exercise_to_plan'),
    path('user', UserList.as_view(), name='user_list'),
    path('user/<pk>', UserDetail.as_view(), name='user_detail')
]


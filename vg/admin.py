from django.contrib import admin
from .models import Profile, Note, Exercise, Day, Plan


admin.site.register(Profile)
admin.site.register(Note)
admin.site.register(Exercise)
admin.site.register(Day)
admin.site.register(Plan)


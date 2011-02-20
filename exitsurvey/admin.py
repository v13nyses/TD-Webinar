from exitsurvey.models import Question, Result, ChooseOne, ChooseMany
from django.contrib import admin

admin.site.register(Question)
admin.site.register(Result)
admin.site.register(ChooseOne)
admin.site.register(ChooseMany)

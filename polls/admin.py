from polls.models import Poll, Choice
from django.contrib import admin

#class ChoiceAdmin(admin.ModelAdmin):
#  fieldsets = [
#    (None, {'fields': ['poll']}),
#    (None, {'fields': ['choice']}),
#  ]

class ChoiceInline(admin.TabularInline):
  model = Choice
  exclude = ('votes',)
  extra = 2

class PollAdmin(admin.ModelAdmin):
  #fieldsets = [
  #  (None, {'fields': ['question']}),
  #  (
  #]
  inlines = [ChoiceInline]
  search_fields = ['question']

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)

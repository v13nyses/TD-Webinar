from django.contrib import admin
from userprofiles.models import UserProfile, ReferType, Title

admin.site.register(UserProfile)
admin.site.register(ReferType)
admin.site.register(Title)

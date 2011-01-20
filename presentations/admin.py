from presentations.models import Presentation, Presenter, PresenterType, Slide, QueuePoint
from django.contrib import admin

admin.site.register(Presentation)
admin.site.register(Presenter)
admin.site.register(PresenterType)
admin.site.register(Slide)
admin.site.register(QueuePoint)

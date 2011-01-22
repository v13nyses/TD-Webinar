from presentations.models import Presentation, Presenter, PresenterType, Slide, QueuePoint, Video
from django.contrib import admin


#class PresentationInline(admin.InlineModelAdmin):
#  model = Presentation
#  extra = 1

#admin.site.register(PresentationInline)
admin.site.register(Presentation)
admin.site.register(Presenter)
admin.site.register(PresenterType)
admin.site.register(Slide)
admin.site.register(QueuePoint)
admin.site.register(Video)

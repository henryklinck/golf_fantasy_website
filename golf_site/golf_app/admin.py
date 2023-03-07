from django.contrib import admin
from .models import BlogPost, Golfer, Team, SeasonSettings
from django.core.exceptions import ValidationError

class SeasonSettingsAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    num_objects = self.model.objects.count()
    if num_objects >= 1:
      return False
    else:
      return True

admin.site.register(BlogPost)
admin.site.register(Golfer)
admin.site.register(Team)
admin.site.register(SeasonSettings, SeasonSettingsAdmin)
# Register your models here.

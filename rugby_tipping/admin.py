from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__','complete', 'date')
    list_filter = ('complete', 'date')
    
    
@admin.register(models.Pick)
class PickAdmin(admin.ModelAdmin):
    list_display = ('match', 'pick_option_string', 'user', 'get_points')
    list_filter = ['user']
admin.site.register(models.Tipper)
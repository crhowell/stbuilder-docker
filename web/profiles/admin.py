from django.contrib import admin

from . import models
# Register your models here.


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.UserApplication)

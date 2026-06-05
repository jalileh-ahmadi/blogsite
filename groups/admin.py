from django.contrib import admin
from .models import Group

class GroupAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        group = form.instance
        group.member.add(group.admin)

admin.site.register(Group, GroupAdmin)

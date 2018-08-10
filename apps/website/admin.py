from django.contrib import admin
from apps.website.models import Members, MemeberPhotos, Activities, PhotoKeywords, ActivityPhotos


class MembersAdmin(admin.ModelAdmin):
    list_display = ('id','username','cellphone','sex','age')

class MemeberPhotosAdmin(admin.ModelAdmin):
    list_display = ('id','memberId','url')

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class ActivityPhotosAdmin(admin.ModelAdmin):
    list_display = ('id','activityId','url')

class PhotoKeywordsAdmin(admin.ModelAdmin):
    list_display = ('id','photoId','keyword')

# Register your models here.
admin.site.register(Members,MembersAdmin)
admin.site.register(MemeberPhotos,MemeberPhotosAdmin)
admin.site.register(Activities,ActivitiesAdmin)
admin.site.register(PhotoKeywords,PhotoKeywordsAdmin)
admin.site.register(ActivityPhotos,ActivityPhotosAdmin)






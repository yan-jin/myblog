from django.contrib import admin
from .models import Post, Pictures, Hole, HoleComment


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'published_date')
    list_filter = ('published_date',)
    filter_horizontal = ('img',)
    ordering = ('published_date',)


class PicturesAdmin(admin.ModelAdmin):
    list_display = ('name',)


class HoleAdmin(admin.ModelAdmin):
    list_display = ('pid', 'text')
    list_filter = ('pid', 'time')
    ordering = ('pid',)


class HoleCommentAdmin(admin.ModelAdmin):
    list_display = ('cid', 'text')
    list_filter = ('cid', 'time')
    ordering = ('cid',)


admin.site.register(Post, PostAdmin)
admin.site.register(Pictures, PicturesAdmin)
admin.site.register(Hole, HoleAdmin)
admin.site.register(HoleComment, HoleCommentAdmin)

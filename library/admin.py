from django.contrib import admin

from .models import Post, Chat, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }


admin.site.register(Chat)
admin.site.register(Category)

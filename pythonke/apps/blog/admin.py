from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_display_links = ['created']
    list_filter = ['updated', 'created']
    search_fields = ['title', 'content']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
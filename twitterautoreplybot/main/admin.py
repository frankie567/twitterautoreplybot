from django.contrib import admin

from .models import Campaign, Query, Action, Tweet, TweetAction, Image

class QueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'correspondingSentence')
    
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

admin.site.register(Campaign)
admin.site.register(Action)
admin.site.register(Tweet)
admin.site.register(TweetAction)
admin.site.register(Query, QueryAdmin)

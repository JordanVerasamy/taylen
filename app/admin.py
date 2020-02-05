from django.contrib import admin

from app.models import User, Emoji, EmojiMatch


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slack_id', 'splitwise_id')


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'image_url', 'record')


@admin.register(EmojiMatch)
class EmojiMatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'winner', 'created_at')

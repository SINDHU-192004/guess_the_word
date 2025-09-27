from django.contrib import admin
from .models import Word, Game, Guess, UserProfile


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['word']
    ordering = ['word']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin', 'games_played', 'games_won', 'win_rate']
    list_filter = ['is_admin', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['games_played', 'games_won', 'created_at']


class GuessInline(admin.TabularInline):
    model = Guess
    extra = 0
    readonly_fields = ['guess_word', 'guess_number', 'feedback', 'created_at']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'status', 'guesses_count', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'word__word']
    readonly_fields = ['created_at', 'completed_at']
    inlines = [GuessInline]


@admin.register(Guess)
class GuessAdmin(admin.ModelAdmin):
    list_display = ['game', 'guess_word', 'guess_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['game__user__username', 'guess_word']
    readonly_fields = ['feedback', 'created_at']

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


class Word(models.Model):
    """Model to store 5-letter words for the game"""
    word = models.CharField(max_length=5, unique=True, help_text="5-letter word in uppercase")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['word']

    @classmethod
    def get_random_word(cls):
        """Get a random active word from the database"""
        active_words = cls.objects.filter(is_active=True)
        if active_words.exists():
            return random.choice(active_words)
        return None


class Game(models.Model):
    """Model to track game sessions"""
    GAME_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=GAME_STATUS_CHOICES, default='ACTIVE')
    guesses_count = models.IntegerField(default=0)
    max_guesses = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.word.word} - {self.status}"

    class Meta:
        ordering = ['-created_at']

    def is_completed(self):
        return self.status in ['WON', 'LOST']

    def can_guess(self):
        return self.status == 'ACTIVE' and self.guesses_count < self.max_guesses

    def complete_game(self, won=False):
        self.status = 'WON' if won else 'LOST'
        self.completed_at = timezone.now()
        self.save()

    @classmethod
    def get_user_games_today(cls, user):
        """Get games played by user today"""
        today = timezone.now().date()
        return cls.objects.filter(
            user=user,
            created_at__date=today
        )

    @classmethod
    def can_user_play_today(cls, user):
        """Check if user can play more games today (max 3 per day)"""
        games_today = cls.get_user_games_today(user).count()
        return games_today < 3


class Guess(models.Model):
    """Model to store individual guesses"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')
    guess_word = models.CharField(max_length=5, help_text="5-letter guess in uppercase")
    guess_number = models.IntegerField()
    feedback = models.JSONField(help_text="Feedback for each letter: correct, wrong_position, incorrect", default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game.user.username} - Guess {self.guess_number}: {self.guess_word}"

    class Meta:
        ordering = ['guess_number']
        unique_together = ['game', 'guess_number']

    def generate_feedback(self):
        """Generate feedback for the guess compared to the target word"""
        target_word = self.game.word.word
        guess_word = self.guess_word
        feedback = []

        # Count letters in target word for wrong position detection
        target_letter_count = {}
        for letter in target_word:
            target_letter_count[letter] = target_letter_count.get(letter, 0) + 1

        # First pass: mark correct positions
        for i in range(5):
            if guess_word[i] == target_word[i]:
                feedback.append('correct')
                target_letter_count[guess_word[i]] -= 1
            else:
                feedback.append('pending')

        # Second pass: mark wrong positions and incorrect
        for i in range(5):
            if feedback[i] == 'pending':
                if guess_word[i] in target_letter_count and target_letter_count[guess_word[i]] > 0:
                    feedback[i] = 'wrong_position'
                    target_letter_count[guess_word[i]] -= 1
                else:
                    feedback[i] = 'incorrect'

        self.feedback = feedback
        return feedback


class UserProfile(models.Model):
    """Extended user profile for game statistics"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Admin' if self.is_admin else 'Player'}"

    def win_rate(self):
        if self.games_played == 0:
            return 0
        return round((self.games_won / self.games_played) * 100, 2)

    def update_stats(self):
        """Update user statistics based on completed games"""
        user_games = Game.objects.filter(user=self.user, status__in=['WON', 'LOST'])
        self.games_played = user_games.count()
        self.games_won = user_games.filter(status='WON').count()
        self.save()

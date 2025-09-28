from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.views.decorators.http import require_http_methods
import json
import random

from .models import Game, Word, Guess, UserProfile
from .forms import CustomUserCreationForm, GuessForm, AdminReportForm


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        # Check if user can play today
        can_play = Game.can_user_play_today(request.user)
        games_today = Game.get_user_games_today(request.user).count()
        
        # Get user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if created or profile.games_played == 0:
            profile.update_stats()
        
        context = {
            'can_play': can_play,
            'games_today': games_today,
            'profile': profile,
        }
        return render(request, 'game/dashboard.html', context)
    
    return render(request, 'game/home.html')


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure user profile exists (signals also handle this)
            UserProfile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


@login_required
def start_game(request):
    """Start a new game"""
    # Check if user can play today
    if not Game.can_user_play_today(request.user):
        messages.error(request, 'You have reached the daily limit of 3 games. Try again tomorrow!')
        return redirect('home')
    
    # Check if user has an active game
    active_game = Game.objects.filter(user=request.user, status='ACTIVE').first()
    if active_game:
        return redirect('play_game', game_id=active_game.id)
    
    # Get a random word
    word = Word.get_random_word()
    if not word:
        messages.error(request, 'No words available. Please contact admin.')
        return redirect('home')
    
    # Create new game
    game = Game.objects.create(user=request.user, word=word)
    messages.success(request, 'New game started! Good luck!')
    return redirect('play_game', game_id=game.id)


@login_required
def play_game(request, game_id):
    """Play the game"""
    game = get_object_or_404(Game, id=game_id, user=request.user)
    
    # If game is completed, redirect to result
    if game.is_completed():
        return redirect('game_result', game_id=game.id)
    
    if request.method == 'POST':
        form = GuessForm(request.POST)
        if form.is_valid():
            guess_word = form.cleaned_data['guess']
            
            # Check if game can accept more guesses
            if not game.can_guess():
                messages.error(request, 'This game is no longer active.')
                return redirect('game_result', game_id=game.id)
            
            # Create guess
            game.guesses_count += 1
            guess = Guess(
                game=game,
                guess_word=guess_word,
                guess_number=game.guesses_count
            )
            
            # Generate feedback
            feedback = guess.generate_feedback()
            guess.save()
            game.save()
            
            # Check if guess is correct
            if guess_word == game.word.word:
                game.complete_game(won=True)
                # Update user profile
                profile = UserProfile.objects.get(user=request.user)
                profile.update_stats()
                return redirect('game_result', game_id=game.id)
            
            # Check if max guesses reached
            if game.guesses_count >= game.max_guesses:
                game.complete_game(won=False)
                # Update user profile
                profile = UserProfile.objects.get(user=request.user)
                profile.update_stats()
                return redirect('game_result', game_id=game.id)
            
            messages.info(request, f'Guess {game.guesses_count} submitted!')
    else:
        form = GuessForm()
    
    # Get all guesses for this game
    guesses = game.guesses.all().order_by('guess_number')
    
    context = {
        'game': game,
        'form': form,
        'guesses': guesses,
        'remaining_guesses': game.max_guesses - game.guesses_count,
    }
    
    return render(request, 'game/play.html', context)


@login_required
def game_result(request, game_id):
    """Show game result"""
    game = get_object_or_404(Game, id=game_id, user=request.user)
    guesses = game.guesses.all().order_by('guess_number')
    
    context = {
        'game': game,
        'guesses': guesses,
        'last_guess': guesses.last(),
    }
    
    return render(request, 'game/result.html', context)


@login_required
def game_history(request):
    """Show user's game history"""
    games = Game.objects.filter(user=request.user, status__in=['WON', 'LOST']).order_by('-created_at')
    
    context = {
        'games': games,
    }
    
    return render(request, 'game/history.html', context)


def is_admin(user):
    """Check if user is admin"""
    if not user.is_authenticated:
        return False
    profile = UserProfile.objects.filter(user=user).first()
    return bool(user.is_staff or (profile and profile.is_admin))


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard"""
    # Get basic stats
    total_users = UserProfile.objects.count()
    total_games = Game.objects.filter(status__in=['WON', 'LOST']).count()
    total_words = Word.objects.filter(is_active=True).count()
    
    # Today's stats
    today = timezone.now().date()
    games_today = Game.objects.filter(created_at__date=today).count()
    users_today = Game.objects.filter(created_at__date=today).values('user').distinct().count()
    
    context = {
        'total_users': total_users,
        'total_games': total_games,
        'total_words': total_words,
        'games_today': games_today,
        'users_today': users_today,
    }
    
    return render(request, 'game/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    """Admin reports"""
    form = AdminReportForm()
    report_data = None
    
    if request.method == 'POST':
        form = AdminReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            
            if report_type == 'daily':
                date = form.cleaned_data['date']
                games = Game.objects.filter(created_at__date=date, status__in=['WON', 'LOST'])
                users_count = games.values('user').distinct().count()
                correct_guesses = games.filter(status='WON').count()
                
                report_data = {
                    'type': 'daily',
                    'date': date,
                    'users_count': users_count,
                    'total_games': games.count(),
                    'correct_guesses': correct_guesses,
                    'success_rate': round((correct_guesses / games.count() * 100) if games.count() > 0 else 0, 2)
                }
            
            elif report_type == 'user':
                user = form.cleaned_data['user']
                games = Game.objects.filter(user=user, status__in=['WON', 'LOST']).order_by('-created_at')
                
                # Group by date
                daily_stats = {}
                for game in games:
                    date = game.created_at.date()
                    if date not in daily_stats:
                        daily_stats[date] = {'total': 0, 'won': 0}
                    daily_stats[date]['total'] += 1
                    if game.status == 'WON':
                        daily_stats[date]['won'] += 1
                
                report_data = {
                    'type': 'user',
                    'user': user,
                    'total_games': games.count(),
                    'games_won': games.filter(status='WON').count(),
                    'daily_stats': daily_stats,
                }
    
    context = {
        'form': form,
        'report_data': report_data,
    }
    
    return render(request, 'game/admin_reports.html', context)


@login_required
@user_passes_test(is_admin)
def manage_words(request):
    """Manage words in the database"""
    words = Word.objects.all().order_by('word')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_word':
            word_text = request.POST.get('word', '').upper().strip()
            if len(word_text) == 5 and word_text.isalpha():
                word, created = Word.objects.get_or_create(word=word_text)
                if created:
                    messages.success(request, f'Word "{word_text}" added successfully!')
                else:
                    messages.warning(request, f'Word "{word_text}" already exists!')
            else:
                messages.error(request, 'Please enter a valid 5-letter word.')
        
        elif action == 'toggle_word':
            word_id = request.POST.get('word_id')
            try:
                word = Word.objects.get(id=word_id)
                word.is_active = not word.is_active
                word.save()
                status = 'activated' if word.is_active else 'deactivated'
                messages.success(request, f'Word "{word.word}" {status}!')
            except Word.DoesNotExist:
                messages.error(request, 'Word not found!')
        
        return redirect('manage_words')
    
    context = {
        'words': words,
    }
    
    return render(request, 'game/manage_words.html', context)


@login_required
@require_http_methods(["POST"]) 
def get_hint(request, game_id):
    """Provide one hint per game: reveal one unrevealed letter position.
    Tracked via session key 'hint_used_<game_id>' to avoid DB migration.
    """
    game = get_object_or_404(Game, id=game_id, user=request.user)
    # If game completed, no hints
    if game.is_completed():
        return JsonResponse({"ok": False, "error": "Game is completed."}, status=400)

    session_key = f"hint_used_{game.id}"
    if request.session.get(session_key):
        return JsonResponse({"ok": False, "error": "Hint already used for this game."}, status=429)

    target = game.word.word
    # Determine positions already correctly revealed
    revealed = set()
    for g in game.guesses.all():
        try:
            fb = g.feedback
        except Exception:
            fb = None
        if not fb:
            continue
        for idx, state in enumerate(fb):
            if state == 'correct':
                revealed.add(idx)

    candidates = [i for i in range(len(target)) if i not in revealed]
    if not candidates:
        return JsonResponse({"ok": False, "error": "All letters already revealed by guesses."}, status=400)

    idx = random.choice(candidates)
    letter = target[idx]

    # Mark hint as used
    request.session[session_key] = True
    request.session.modified = True

    return JsonResponse({"ok": True, "index": idx, "letter": letter})

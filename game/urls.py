from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Game pages
    path('start-game/', views.start_game, name='start_game'),
    path('play/<int:game_id>/', views.play_game, name='play_game'),
    path('play/<int:game_id>/hint/', views.get_hint, name='get_hint'),
    path('result/<int:game_id>/', views.game_result, name='game_result'),
    path('history/', views.game_history, name='game_history'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),
    path('manage-words/', views.manage_words, name='manage_words'),
]

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('main',views.landing, name='landing'),
    path('',views.home,name='home'),
    path('search',views.home_search, name='home-search'),
    path('notifications',views.notifications, name='notifications'),

    path('questions/Newest',views.question_list,name='question-list'),
    path('questions/tab=Popular',views.popular_quest,name='popular-quest'),
    path('questions/tab=Recommend',views.recommend_quest,name='recommend-list'),
    path('questions/tab=Unanswered',views.unanswer,name='unanswered'),

    path('question/<int:id>/<str:slug>',views.detail,name='detail'),

    path('<int:cat_id>/<str:title>', views.category_quest, name="category-quest"),
    path('save-comment',views.save_comment,name='save-comment'),
    path('save-upvote',views.save_upvote,name='save-upvote'),
    path('save-downvote',views.save_downvote,name='save-downvote'),
    # User Register
    path('accounts/register/',views.register,name='register'),
    path('accounts/login/',views.loginView,name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name=
            'password-reset/password_reset_form.html'), name='reset_password'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name=
            'password-reset/password_reset_complete.html'), name= 'password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name=
            'password-reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name=
            'password-reset/password_reset_done.html'),name='password_reset_complete'),
    # Profile
    path('user/<int:id>/<str:username>/',views.profile,name='profile'),
    path('accounts/profile/edit/',views.profile_edit,name='profile-edit'),
    # Ask QUestion
    path('ask-question',views.ask_form,name='ask-question'),
    path('edit-question/<int:id>',views.quest_edit,name='quest-edit'),
    # Tag Page
    path('tag/<str:tag>',views.tag,name='tag'),
    # Tags Page
    path('tags',views.tags,name='tags'),

    path('users',views.users,name='users'),
    path('users/tab=Newest',views.new_users,name='new-users'),
    path('users/tab=Moderators',views.moderator,name='moderators'),

    path('badges',views.badges,name='badges'),

    path('contact',views.contact,name='contact'),
    path('faq',views.faq,name='faq'),
    path('about',views.about,name='about'),
    path('privacy-policy',views.privacy_policy,name='privacy-policy'),
    path('terms',views.terms,name='terms'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
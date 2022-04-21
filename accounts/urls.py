from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('profile/', views.profile_view, name="profile"),
    path('edit-profile/', views.edit_profile_view, name="edit_profile"),
    path('change-password/', views.change_password_view, name="change_password"),
    path('dashboard/<int:user_id>/', views.dashboard_view, name="dashboard"),
    path('users/', views.users_view, name="users")

    # url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     core_views.activate, name='activate'),
]

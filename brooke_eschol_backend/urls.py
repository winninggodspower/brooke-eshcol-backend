from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_authentication.urls')),
    path('', include('member.urls')),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'), 

    path('verification/', include('verify_email.urls')),

    path('accounts/', include('allauth.urls')),
]

handler404 = 'user_authentication.views.error_404_view'

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)


from django.contrib import admin
from django.urls import path,include
from polls.views import GoogleSocialAuthView

urlpatterns = [
    path('',include('polls.urls')),
    path('admin/', admin.site.urls),
    # OAuth
    path('social-auth/', include('social_django.urls', namespace='social')),
    # OAuth2
    path('auth/',include('drf_social_oauth2.urls', namespace='drf')),
    # OAuth
    path('google/', GoogleSocialAuthView.as_view()),
]
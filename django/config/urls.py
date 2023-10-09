from django.contrib import admin
from django.urls import path,include
from polls.apis import GoogleSocialAuthView

urlpatterns = [
    path('',include('polls.urls')),
    path('admin/', admin.site.urls),
    # OAuth2
    path('auth/',include('drf_social_oauth2.urls', namespace='drf')),
    # OAuth
    path('google/', GoogleSocialAuthView.as_view()),
]
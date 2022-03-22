"""gigle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social.urls')),
    path('social/', include('organiser.urls')),
    path('calendar/', include('gig_calendar.urls')),
]

# error handle pages
# page not found
handler404 = 'social.views.handle_404'
# server error
handler500= 'social.views.handle_500'
# permission error
handler403 = 'social.views.handle_403'
# bad request error
handler400 = 'social.views.handle_400'


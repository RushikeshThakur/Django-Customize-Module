"""djcus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#from django.conf.urls import path,include
from django.urls import path, re_path
from accounts.views import activate_user_view, register, home, user_login, user_logout, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('home/', home, name="home"),
    path('logout/', user_logout, name="logout"),
    path('profile/', profile_view, name="profile"),
    re_path(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name="activate"),
]

# If you are using multiple path pattern in 3.0 you shoud go with re_path
from django.urls import path
from . import views
#from .views import MainView, CompareView, ItemView

urlpatterns = [
    path('', views.home, name="home"),
    path('create', views.create, name="create"),
    path('results', views.results, name="results"),
    path('vote', views.vote, name="vote"),
    path('recoreded', views.recorded, name="recorded"),
    path('login', views.login_page, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_user, name="logout"),
    #path('', MainView.as_view(), name="main"),
    #path('compare/', CompareView.as_view(), name="compare"),
    #path('item_info/<int:pk>', ItemView.as_view(), name="item_info"),
]

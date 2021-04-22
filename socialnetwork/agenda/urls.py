from django.urls import path
from agenda.views import AgendaListAPIView, AgendaDetailsAPIView
from agenda.views import HomeListView,TrendingListView, agenda_detail
from agenda.views import create_agenda,Logout,user_profile,login_user,register_user
from agenda.views import user_follower,user_following,follow_user,unfollow_user
#AgendaDetailView,

urlpatterns = [
    path('',HomeListView.as_view(),name = 'home'),
    path('api/agenda/',AgendaListAPIView.as_view()),
    path('api/agenda/<int:id>/',AgendaDetailsAPIView.as_view()),
   # path('users/<str:username>', UserDetailView.as_view(),name='profile_view'),
    path('users/<str:username>', user_profile,name='profile_view'),
    path('users/<str:username>/followers', user_follower,name='followers'),
    path('users/<str:username>/following', user_following,name='following'),
    path('agendas/<slug:slug>', agenda_detail,name='agenda_view'),    
    path('trending/',TrendingListView.as_view(),name = 'trending'),
    path('create/',create_agenda,name = 'create'),
    path('follow/<str:username>', follow_user,name='follow'),
    path('unfollow/<str:username>', unfollow_user,name='unfollow'),
    path('login/',login_user,name = 'login'),
    path('register/',register_user,name  = 'register'),
    path('logout/',Logout,name = 'logout')
]

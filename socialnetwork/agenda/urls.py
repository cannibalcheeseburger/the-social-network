from django.urls import path
from agenda.views import AgendaListAPIView, AgendaDetailsAPIView
from agenda.views import HomeListView,AgendaDetailView,TrendingListView
from agenda.views import create_agenda,Logout,user_profile


urlpatterns = [
    path('',HomeListView.as_view(),name = 'home'),
    path('api/agenda/',AgendaListAPIView.as_view()),
    path('api/agenda/<int:id>/',AgendaDetailsAPIView.as_view()),
   # path('users/<str:username>', UserDetailView.as_view(),name='profile_view'),
    path('users/<str:username>', user_profile,name='profile_view'),
    path('agendas/<slug:slug>', AgendaDetailView.as_view(),name='agenda_view'),    
    path('trending/',TrendingListView.as_view(),name = 'trending'),
    path('create/',create_agenda,name = 'create'),
    path('logout/',Logout,name = 'logout')
]

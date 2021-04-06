from django.urls import path
from agenda.views import AgendaListAPIView, AgendaDetailsAPIView,HomeListView,UserDetailView


urlpatterns = [
    path('',HomeListView.as_view(),name = 'home'),
    path('api/agenda/',AgendaListAPIView.as_view()),
    path('api/agenda/<int:id>/',AgendaDetailsAPIView.as_view()),
    path('users/<str:username>', UserDetailView.as_view(),name='profile_view'),    
]

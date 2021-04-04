from django.urls import path
from agenda.views import AgendaList, AgendaDetails,home


urlpatterns = [
    path('api/agenda/',AgendaList.as_view()),
    path('api/agenda/<int:id>/',AgendaDetails.as_view()),
    path('',home,name = 'home')
]

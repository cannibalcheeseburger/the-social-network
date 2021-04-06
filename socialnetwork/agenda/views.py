from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView
from agenda.api.serializers import AgendaSerializer
from agenda.models import Agenda,Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


class AgendaListAPIView(APIView):
    def get(self,request):
        agendas = Agenda.objects.all()
        serializer = AgendaSerializer(agendas,many = True)
        return Response(serializer.data)



class AgendaDetailsAPIView(APIView):
    def get_object(self,id):
        try:
            return Agenda.objects.get(id=id)
        except Agenda.DoesNotExist:
            return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        agenda = self.get_object(id)
        serializer = AgendaSerializer(agenda)
        return Response(serializer.data)

    def put(self,request,id):
        agenda = self.get_object(id)
        serializer = AgendaSerializer(agenda,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class HomeListView(ListView):
    model = Agenda
    template_name = 'social.html'
    context_object_name = 'posts'


class UserDetailView(DetailView):
    model = Users
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self):
        return Users.objects.get(username=self.kwargs.get("username"))


class AgendaDetailView(DetailView):
    model = Agenda
    template_name = 'agenda.html'
    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            agenda = Agenda.objects.get(slug=self.kwargs.get("slug"))
            context['agenda'] = agenda
            context['Ayes'] = agenda.ayes.all().count()
            context['Nays'] = agenda.nays.all().count()

            return context
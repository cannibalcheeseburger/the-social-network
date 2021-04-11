from django.shortcuts import render
from django.views.generic import ListView
from agenda.api.serializers import AgendaSerializer
from agenda.models import Agenda
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

class AgendaList(APIView):
    def get(self,request):
        agendas = Agenda.objects.all()
        serializer = AgendaSerializer(agendas,many = True)
        return Response(serializer.data)

class AgendaDetails(APIView):
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

def home(request):
    context = {
        'posts' :Agenda.objects.all()
        }
    return render(request,'social.html',context=context)
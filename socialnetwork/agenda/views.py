from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView,DetailView
from agenda.api.serializers import AgendaSerializer
from agenda.models import Agenda,Users,Aye,Nay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Count
from .forms import AgendaCreateForm
from django.contrib.auth import logout

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

"""
class UserDetailView(DetailView):
    model = Users
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self):
        return Users.objects.get(username=self.kwargs.get("username"))
"""

def user_profile(request,username):
    user = Users.objects.get(username = username)
    posts = Agenda.objects.filter(author=user)
    context = {'user':user,
                'posts':posts}
    return render(request,'profile.html',context)

class AgendaDetailView(DetailView):
    model = Agenda
    template_name = 'agenda.html'
    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            agenda = Agenda.objects.get(slug=self.kwargs.get("slug"))
            context['agenda'] = agenda
            context['Ayes'] = Aye.objects.filter(agenda=agenda).count()
            context['Nays'] = Nay.objects.filter(agenda=agenda).count()
            return context

class TrendingListView(ListView):
    template_name = 'trending.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return Agenda.objects.annotate(total_aye = Count('aye')).order_by('-total_aye')



def create_agenda(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = AgendaCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['Title']
            Text = form.cleaned_data['Text']
            user = request.user
            agenda = Agenda(title=title,text = Text,author = user)
            agenda.save()
            return redirect('home')
    form = AgendaCreateForm()
    return render(request, 'create.html',{'form':form})


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
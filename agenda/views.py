from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView,DetailView
from agenda.api.serializers import AgendaSerializer
from agenda.models import Agenda,Users,Aye,Nay,UserFollowing
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Count
from .forms import AgendaCreateForm,LoginForm,RegisterForm,AyeCommentForm,NayCommentForm,EditProfileForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.hashers import make_password

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
    ordering = ['-id']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            follower_user_ids = UserFollowing.objects.filter(following_user_id = self.request.user)\
                                                    .values_list('user_id', flat=True)\
                                                    .distinct()
            if  follower_user_ids:
                agenda = Agenda.objects.filter(author_id__in=follower_user_ids)
                return agenda
        agenda = Agenda.objects.all().order_by('-date')
        return agenda

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
    if request.user.is_authenticated:
        context['is_following'] = UserFollowing.objects.filter(following_user=request.user).filter(user=user).exists()
        context['followers_count'] = UserFollowing.objects.filter(user=user).count()
        context['following_count'] = UserFollowing.objects.filter(following_user=user).count()

    return render(request,'profile.html',context)
"""
class AgendaDetailView(DetailView):
    model = Agenda
    template_name = 'agenda.html'
    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            agenda = Agenda.objects.get(slug=self.kwargs.get("slug"))
            context['agenda'] = agenda
            context['Ayes'] = Aye.objects.filter(agenda=agenda)
            context['Nays'] = Nay.objects.filter(agenda=agenda)
            return context
"""

def edit_profile(request):
    if request.user.is_authenticated:
        form = EditProfileForm()
        user = Users.objects.get(username=request.user.username)
        if request.method == 'POST':
            form = EditProfileForm(request.POST,instance = user)
            if form.is_valid():
                form.save()
                return redirect('profile_view',username = request.user.username)
        return render(request,'edit_profile.html',{'form':form})
    else:
        return redirect('login')

def agenda_detail(request,slug):
    agenda = Agenda.objects.get(slug=slug)
    context = {}
    context['agenda'] = agenda
    context['Ayes'] = Aye.objects.filter(agenda=agenda)
    context['Nays'] = Nay.objects.filter(agenda=agenda)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form1 = AyeCommentForm(request.POST)
        form2 = NayCommentForm(request.POST)
        if "naybt" in request.POST:        
            if form2.is_valid():
                comment = form2.cleaned_data['comment']
                nay = Nay(user=request.user,comments=comment,agenda=agenda)
                nay.save()
        if "ayebt" in request.POST:
            if form1.is_valid():
                comment = form1.cleaned_data['comment']
                aye = Aye(user=request.user,comments=comment,agenda=agenda)
                aye.save()
                return render(request, 'agenda.html',context)
        
      
                return render(request, 'agenda.html',context)

    form1 = AyeCommentForm()
    form2 = NayCommentForm()
    context['form1'] = form1
    context['form2'] = form2 
    return render(request, 'agenda.html',context)



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
"""
def login_user(request):
    user = Users.objects.get(username='ranu')
    password = make_password('123')
    user.password = password
    user.save()
"""
def login_user(request):
    if request.method == 'POST':
        form_l = LoginForm(request.POST)
        if form_l.is_valid():
            username = form_l.cleaned_data['username']
            password = form_l.cleaned_data['password']
            user = authenticate(username=username, password=password)           
            if user is not None:
                login(request, user)
                return redirect('home')
    form_l = LoginForm()
    return render(request, 'login.html',{'form_l':form_l})

def register_user(request):
    if request.method == 'POST':
        form_r = RegisterForm(request.POST)
        if form_r.is_valid():
            username = form_r.cleaned_data['username']
            email = form_r.cleaned_data['email']

            password1 = form_r.cleaned_data['password1']
            password2 = form_r.cleaned_data['password2']
            if password1 == password2:
                password = make_password(password1)
                user = Users(username=username,email=email,password=password)
                user.save()
                return redirect('login')
    form_r = RegisterForm()
    return render(request, 'register.html',{'form_r':form_r})


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def user_follower(request,username):
    followers = UserFollowing.objects.filter(user=username)
    return render(request,'followers.html',{'followers':followers})

def user_following(request,username):
    followings = UserFollowing.objects.filter(following_user=username)
    return render(request,'followings.html',{'followings':followings})

def follow_user(request,username):
    if request.user.is_authenticated:
        user = Users.objects.get(username=username)
        is_following= UserFollowing.objects.filter(following_user=request.user).filter(user=user).exists()
        if not is_following:
            follow = UserFollowing(user=user,following_user=request.user)
            follow.save()
            
        return redirect('profile_view',username = username)
    else:
        return redirect('login')


def unfollow_user(request,username):
    if request.user.is_authenticated:
        user = Users.objects.get(username=username)
        is_following= UserFollowing.objects.filter(following_user=request.user).filter(user=user).exists()
        if  is_following:
            follow = UserFollowing.objects.get(user=user,following_user=request.user)
            follow.delete()
        return redirect('profile_view',username=username)

    else:
        return redirect('login')
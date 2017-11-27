from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import View
from music import models
from .models import Album
from .forms import UserForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    template_name = 'music/details.html'
    model = Album

class createAlbum(CreateView):
    model = Album
    fields= ['artist','album_title','genre','album_logo']


class updateAlbum(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

class deleteAlbum(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form' : form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None :

                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

        return render(request,self.template_name,{'form' : form})


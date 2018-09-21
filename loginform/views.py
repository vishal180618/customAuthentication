# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import forms, Form
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django import http
from django.contrib import auth
from django.views import View
from django.views.generic import FormView

from loginform.models import User
from .forms import LoginForm,RegisterForm
from django.contrib.auth.hashers import make_password

class LogoutPage(FormView):
    pass


class LoginPage(FormView):
    pass


class SignUp(FormView):
    template_name='signup.html'
    def get(self, request, *args, **kwargs):
        super(SignUp, self).get(request, args, kwargs)
        context_data = self.get_context_data()
        return self.render_to_response(self.get_context_data())




def logout_page(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return http.HttpResponse("you have successfuly logged out of the website")
    else:
        return http.HttpResponse("you are not logged in!!")

def login_page(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            auth.login(request,form.user)
            return http.HttpResponseRedirect('/home/')

    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            getemail = form.cleaned_data['email']
            getPass = make_password(form.cleaned_data['password'], None, 'md5')
            user = User(email=getemail, password=getPass)
            user.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('Yayyy!!! your account is created successfully')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})

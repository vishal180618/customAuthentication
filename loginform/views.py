# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from loginform.models import User
from .forms import LoginForm, RegisterForm, BookForm
from django.views.generic import TemplateView, DetailView, ListView, CreateView, DeleteView, UpdateView
from models import Book

class LogoutPage(FormView):
    pass


class LoginPage(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    get_success_url = 'http://127.0.0.1:8000/home/'

    def form_valid(self, form):
        auth.login(self.request, form.user)
        return HttpResponseRedirect('http://127.0.0.1:8000/home/')


class SignUp(FormView):
    template_name = 'signup.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user_name = form.cleaned_data['email']
        user_password = make_password(form.cleaned_data['password'])
        user = User(email=user_name, password=user_password)
        user.save()
        return HttpResponse("you account has been created successfully --django")


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


# def signup(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = RegisterForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             getemail = form.cleaned_data['email']
#             getPass = make_password(form.cleaned_data['password'], None, 'md5')
#             user = User(email=getemail, password=getPass)
#             user.save()
#
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponse('Yayyy!!! your account is created successfully')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = RegisterForm()
#
#     return render(request, 'signup.html', {'form': form})


class HomePage(ListView):
    template_name = 'loginform/home.html'
    model = Book


class BookDetail(DetailView):
    template_name = 'loginform/book_detail.html'
    model = Book


class UpdateBookDetail(UpdateView):
    form_class = BookForm
    model = Book
    success_url = reverse_lazy('loginform:book_list')


class DeleteBook(DeleteView):
    model = Book
    success_url = reverse_lazy('loginform:book_list')


class AddBook(CreateView):
    form_class = BookForm
    template_name = 'loginform/addbook_form.html'
    success_url = reverse_lazy('loginform:book_list')

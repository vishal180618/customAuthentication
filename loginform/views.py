# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.views.generic import FormView

from loginform.models import User
from models import Book
from .forms import LoginForm, RegisterForm, BookForm


class LogoutPage(FormView):
    pass


class LoginPage(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    get_success_url = 'http://127.0.0.1:8000/home/'

    def form_valid(self, form):
        auth.login(self.request, form.user)
        return HttpResponseRedirect(reverse_lazy('loginform:book_list'))


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


class HomePage(LoginRequiredMixin, ListView):
    login_url = '/Login/'
    permission_denied_message = 'not allowed to view this page'
    template_name = 'loginform/home.html'
    model = Book


class BookDetail(LoginRequiredMixin, DetailView):
    template_name = 'loginform/book_detail.html'
    model = Book


class UpdateBookDetail(LoginRequiredMixin, UpdateView):
    form_class = BookForm
    model = Book
    success_url = reverse_lazy('loginform:book_list')


class DeleteBook(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('loginform:book_list')


class AddBook(LoginRequiredMixin, CreateView):
    form_class = BookForm
    template_name = 'loginform/addbook_form.html'
    success_url = reverse_lazy('loginform:book_list')

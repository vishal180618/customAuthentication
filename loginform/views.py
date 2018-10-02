# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView, FormView

from loginform.models import User
from models import Book
from .forms import LoginForm, RegisterForm, BookForm


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
    success_url = reverse_lazy('loginform:book_list')

    def form_valid(self, form):
        user_name = form.cleaned_data['email']
        user_password = make_password(form.cleaned_data['password'])
        user = User(email=user_name, password=user_password)
        user.save()
        return HttpResponseRedirect(self.success_url)


def logout_page(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return http.HttpResponse("you have successfuly logged out of the website")
    else:
        return http.HttpResponse("you are not logged in!!")


class HomePage(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('loginform:login')
    permission_denied_message = 'not allowed to view this page'
    template_name = 'loginform/home.html'
    def get_queryset(self):
        try:
            queryset = Book.objects.filter(user_id=self.request.user.id)
        except :
            return HttpResponseRedirect(reverse_lazy('loginform:book_list'))

        return queryset



class BookDetail(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('loginform:login')
    template_name = 'loginform/book_detail.html'

    def get_queryset(self):
        if Book.objects.get(pk=self.kwargs.get('pk')).user_id != self.request.user.id:
            raise Http404
        else:
            queryset = Book.objects.filter(pk=self.kwargs.get('pk'), user_id=self.request.user.id)
        return queryset


class UpdateBookDetail(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('loginform:login')
    form_class = BookForm
    success_url = reverse_lazy('loginform:book_list')

    def get_queryset(self):
        if Book.objects.get(pk=self.kwargs.get('pk')).user_id != self.request.user.id:
            raise Http404
        else:
            queryset = Book.objects.filter(pk=self.kwargs.get('pk'), user_id=self.request.user.id)
        return queryset


class DeleteBook(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('loginform:login')
    success_url = reverse_lazy('loginform:book_list')

    def get_queryset(self):
        if Book.objects.get(pk=self.kwargs.get('pk')).user_id != self.request.user.id:
            raise Http404
        else:
            queryset = Book.objects.filter(pk=self.kwargs.get('pk'), user_id=self.request.user.id)
        return queryset


class AddBook(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('loginform:login')
    form_class = BookForm
    template_name = 'loginform/addbook_form.html'
    success_url = reverse_lazy('loginform:book_list')

    def form_valid(self, form):
        form.user = self.request.user
        return super(AddBook, self).form_valid(form)

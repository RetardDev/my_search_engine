from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.views import View

class Index(View):
    def get(self, request):
        return render(request, 'index.html')
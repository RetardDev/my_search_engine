from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from datetime import datetime
class Log(View):
    @staticmethod
    def log_click(ip_address, query, clciked_url):
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp}, IP: {ip_address}, QUERY: {query}, CLICKED {clciked_url}\n"
        with open('Logs.txt', 'a') as logFile:
            logFile.write(log_entry)

    def get(self, request):
        clicked_url = request.GET.get('url', '')
        query = request.GET.get('query', '')
        ip_address = request.META.get('REMOTE_ADDR')
        self.log_click(ip_address, query, clicked_url)
        return redirect(clicked_url)
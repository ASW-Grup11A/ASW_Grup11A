from django.http import HttpResponse
from django.shortcuts import render

from empo_news.forms import SubmitForm


def index(request):
    return HttpResponse("Hello, world. You're at the empo_news index.")


def submit(request):
    return render(request, 'empo_news/submit.html')


def formTest(request):
    form = SubmitForm()
    context = {
        'form': form,
    }
    return render(request, 'empo_news/formtest.html', context)

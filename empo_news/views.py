from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from empo_news.forms import SubmitForm
from empo_news.models import Contribution


def index(request):
    return HttpResponse("Hello, world. You're at the empo_news index.")


def submit(request):
    form = SubmitForm()
    submit_response = request.POST

    if submit_response.get('submit_button'):
        contribution = Contribution(None, 'Albert', submit_response.get('title'), 1, date.today(), submit_response.get('url'),
                                    None, 0)
        contribution.save()
        return HttpResponseRedirect(reverse('empo_news:main_page_logged'))

    context = {
        'form': form,
    }
    return render(request, 'empo_news/submit.html', context)

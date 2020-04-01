from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from empo_news.forms import SubmitForm
from empo_news.models import Contribution, User


def submit(request):
    form = SubmitForm()

    if request.method == 'POST':
        form = SubmitForm(request.POST)

        if form.is_valid():
            contribution = Contribution(user=User(username="Pepe05"), title=form.cleaned_data['title'],
                                        publication_time=date.today())
            if form.cleaned_data['url'] and SubmitForm.valid_url(form.cleaned_data['url']):
                contribution.url = form.cleaned_data['url']
            else:
                contribution.text = form.cleaned_data['text']
            contribution.save()

            return HttpResponseRedirect(reverse('empo_news:main_page'))

    context = {
        'form': form
    }
    return render(request, 'empo_news/submit.html', context)


def main_page(request):
    most_points_list = Contribution.objects.order_by('-points')[:29]
    context = {
        "list": most_points_list,
        "user": User(username="Pepe05")
    }
    return render(request, 'empo_news/main_page_logged.html', context)


def new_page(request):
    most_recent_list = Contribution.objects.order_by('-publication_time')[:29]
    context = {
        "list": most_recent_list,
        "user": User(username="Pepe05"),
        "highlight": "new"
    }
    return render(request, 'empo_news/main_page_logged.html', context)


def not_implemented(request):
    return HttpResponse('View not yet implemented')

def item(request):
    if request.method == 'GET':
        contribution_id = request.GET.get('id', '')
        contribution = Contribution.objects.get(id=contribution_id)
        context = {
            "contribution": contribution
        }
        return render(request, 'empo_news/contribution.html', context)

    return HttpResponseRedirect(reverse('empo_news:main_page'))


from datetime import date

from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse

from empo_news.forms import SubmitForm
from empo_news.models import Contribution, UserFields


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
        # "user": User(username="Pepe05")
    }
    return render(request, 'empo_news/main_page.html', context)


def new_page(request):
    most_recent_list = Contribution.objects.order_by('-publication_time')[:29]
    context = {
        "list": most_recent_list,
        # "user": User(username="Pepe05"),
        "highlight": "new"
    }
    return render(request, 'empo_news/main_page_logged.html', context)


def not_implemented(request):
    return HttpResponse('View not yet implemented')


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')


def profile(request):
    if date.today() != request.user.date_joined:
        userFields = UserFields(user=request.user)
        userFields.save()
    else:
        userFields = UserFields(user=request.user, karma=1, about="",
                                showdead=False, noprocrast=False, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    context = {
        "userFields": userFields
    }
    return render(request, 'empo_news/profile.html', context)


def updateUserFields(request, about, showdead, noprocast, maxvisit, minaway, delay):
    context = {
        "userFields": UserFields(request.user)
    }
    return render(request, 'empo_news/profile.html', context)

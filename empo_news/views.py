from datetime import date

from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse
from pyasn1.compat.octets import null

from empo_news.forms import SubmitForm, UserUpdateForm
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
    do_logout(request)
    return redirect('/')


def profile(request):
    if UserFields.objects.filter(user=request.user).count() == 0:
        userFields = UserFields(user=request.user, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    else:
        userFields = UserFields.objects.get(user=request.user)

    if userFields.showdead == 0:
        posS = '0'
    else:
        posS = '1'

    if userFields.noprocrast == 0:
        posN = '0'
    else:
        posN = '1'

    form = UserUpdateForm(initial={'email': request.user.email, 'karma': userFields.karma, 'about': userFields.about,
                                   'showdead': posS, 'noprocrast': posN, 'maxvisit': userFields.maxvisit,
                                   'minaway': userFields.minaway, 'delay': userFields.delay})

    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['showdead'])
            UserFields.objects.filter(user=request.user).update(user=request.user, about=form.cleaned_data['about'],
                                                                showdead=form.cleaned_data['showdead'],
                                                                noprocrast=form.cleaned_data['noprocrast'],
                                                                maxvisit=int(form.cleaned_data['maxvisit']),
                                                                minaway=int(form.cleaned_data['minaway']),
                                                                delay=int(form.cleaned_data['delay']))
            User.objects.filter(username=request.user.username).update(email=form.cleaned_data['email'])

            return HttpResponseRedirect(reverse('empo_news:user_page'))
    context = {
        "form": form,
        "userFields": userFields
    }
    return render(request, 'empo_news/profile.html', context)

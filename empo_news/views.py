from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from empo_news.forms import SubmitForm
from empo_news.models import Contribution


def submit(request):
    form = SubmitForm()

    if request.method == 'POST':
        form = SubmitForm(request.POST)

        if form.is_valid():
            contribution = Contribution(user=request.user, title=form.cleaned_data['title'],
                                        publication_time=datetime.today(), text='')
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
    update_show(Contribution.objects.order_by('-points'), request.user.id, 30)
    most_points_list = Contribution.objects.filter(show=True).order_by('-points')[:30]
    more = len(Contribution.objects.filter(show=True)) > 30
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "main_page",
        "more": more,
        "next_page": "empo_news:main_page_pg",
        "page_value": 1,
        "next_page_value": 2,
        "base_loop_count": 0,
    }
    return render(request, 'empo_news/main_page.html', context)


def main_page_pg(request, pg):
    if pg <= 1:
        return HttpResponseRedirect(reverse('empo_news:main_page'))
    update_show(Contribution.objects.order_by('-points'), request.user.id, pg * 30)
    most_points_list = Contribution.objects.filter(show=True).order_by('-points')[((pg - 1) * 30)+1:(pg * 30)]
    more = len(Contribution.objects.filter(show=True)) > (pg * 30)
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "main_page_pg",
        "more": more,
        "next_page": "empo_news:main_page_pg",
        "page_value": pg,
        "next_page_value": pg+1,
        "base_loop_count": (pg-1)*30,
    }
    return render(request, 'empo_news/main_page.html', context)


def new_page(request):
    update_show(Contribution.objects.order_by('-publication_time'), request.user.id, 30)
    most_recent_list = Contribution.objects.filter(show=True).order_by('-publication_time')[:30]
    more = len(Contribution.objects.filter(show=True)) > 30
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "new_page",
        "highlight": "new",
        "more": more,
        "next_page": "empo_news:new_page_pg",
        "page_value": 1,
        "next_page_value": 2,
        "base_loop_count": 0,
    }
    return render(request, 'empo_news/main_page.html', context)


def new_page_pg(request, pg):
    if pg <= 1:
        return HttpResponseRedirect(reverse('empo_news:new_page'))
    update_show(Contribution.objects.order_by('-publication_time'), request.user.id, (pg * 30))
    most_recent_list = Contribution.objects.filter(show=True).order_by('-publication_time')[
                       ((pg - 1) * 30) + 1:(pg * 30)]
    more = len(Contribution.objects.filter(show=True)) > (pg * 30)
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "new_page_pg",
        "highlight": "new",
        "more": more,
        "next_page": "empo_news:new_page_pg",
        "page_value": pg,
        "next_page_value": pg+1,
        "base_loop_count": (pg-1)*30,
    }
    return render(request, 'empo_news/main_page.html', context)


def likes(request, view, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user);
    else:
        contribution.likes.add(request.user)
    contribution.points = contribution.total_likes()
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view))
    return HttpResponseRedirect(reverse('empo_news:' + view, args=(pg,)))


def hide(request, view, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.hidden.filter(id=request.user.id).exists():
        contribution.hidden.remove(request.user);
    else:
        contribution.hidden.add(request.user)
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view))
    return HttpResponseRedirect(reverse('empo_news:' + view, args=(pg,)))


def not_implemented(request):
    return HttpResponse('View not yet implemented')


def item(request):
    if request.method == 'GET':
        contribution_id = int(request.GET.get('id', -1))
        try:
            contribution = Contribution.objects.get(id=contribution_id)
            context = {
                "contribution": contribution
            }
            return render(request, 'empo_news/contribution.html', context)
        except Contribution.DoesNotExist:
            return HttpResponse('No such item.')

    return HttpResponseRedirect(reverse('empo_news:main_page'))


def update_show(all_contributions, userid, border):
    count_shown = 0
    i = 0
    length = len(all_contributions)
    while count_shown < border and i < length:
        contribution = all_contributions[i]
        if contribution.hidden.filter(id=userid).exists():
            contribution.show = False
        else:
            contribution.show = True
            count_shown += 1
        contribution.save()
        i += 1

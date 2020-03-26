from django.http import HttpResponse
from django.shortcuts import render
from empo_news.models import Contribution, User


def main_page(request):
    most_points_list = Contribution.objects.order_by('-points')[:29]
    context = {
        "list": most_points_list,
    }
    return render(request, 'empo_news/main_page.html', context);


def new_page(request):
    most_recent_list = Contribution.objects.order_by('-publication_time')[:29]
    context = {
        "list": most_recent_list,
    }
    return render(request, 'empo_news/main_page.html', context);


def not_implemented(request):
    return HttpResponse('View not yet implemented');

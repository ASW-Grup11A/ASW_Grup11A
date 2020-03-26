from django.http import HttpResponse
from django.shortcuts import render

from empo_news.models import Contribution


def main_page(request):
    most_points_list = Contribution.objects.order_by('-points')[:29]
    context = {
        "list": most_points_list,
    }
    return render(request, 'empo_news/main_page.html', context);


def not_implemented(request):
    return HttpResponse('View not yet implemented');

from django.http import HttpResponse
from django.shortcuts import render

from empo_news.forms import SubmitForm


def index(request):
    return HttpResponse("Hello, world. You're at the empo_news index.")


def submit(request):
    form = SubmitForm()
    submit_response = request.POST

    if submit_response.get('submit_button'):
        if form.is_valid():
            print("VALID")

    context = {
        'form': form,
    }
    return render(request, 'empo_news/submit.html', context)

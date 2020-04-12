from datetime import datetime

from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from empo_news.forms import SubmitForm, CommentForm, UserUpdateForm, EditCommentForm
from empo_news.models import Contribution, UserFields, Comment


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
            contribution.likes.add(request.user)
            contribution.save()

            return HttpResponseRedirect(reverse('empo_news:main_page'))

    context = {
        'form': form
    }
    return render(request, 'empo_news/submit.html', context)


def main_page(request):
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.exclude(title__isnull=True)
    update_show(contributions.order_by('-points'), request.user.id, pg * 30)
    most_points_list = contributions.filter(show=True).order_by('-points')[list_base:(pg * 30)]
    more = len(contributions.filter(show=True)) > (pg * 30)
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "main_page",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
    }
    return render(request, 'empo_news/main_page.html', context)


def new_page(request):
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.exclude(title__isnull=True)
    update_show(contributions.order_by('publication_time'), request.user.id, pg * 30)
    most_recent_list = contributions.filter(show=True).order_by('publication_time')[list_base:(pg * 30)]
    more = len(contributions.filter(show=True)) > (pg * 30)
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "new_page",
        "highlight": "new",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
    }
    return render(request, 'empo_news/main_page.html', context)


def submitted(request):
    user_id = request.GET.get('id', "")
    if not User.objects.filter(username=user_id).exists():
        return HttpResponse('No such user')
    base_list = User.objects.get(username=user_id).contribution

    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('&')[0]
    list_start = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_start = 0

    submitted_list = base_list.order_by('publication_time')[list_start:(pg * 30)]
    more = len(base_list.all()) > (pg * 30)
    for contribution in submitted_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()

    context = {
        "list": submitted_list,
        "user": request.user,
        "mine": (request.user.username == user_id),
        "path": "submitted",
        "submitted_id": user_id,
        "highlight": "submitted",
        "more": more,
        "next_page": base_path + "&pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
    }
    return render(request, 'empo_news/submitted.html', context)


def likes_submit(request, view, id, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user);
    else:
        contribution.likes.add(request.user)
    contribution.points = contribution.total_likes()
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view) + '?id=' + id)
    return HttpResponseRedirect(reverse('empo_news:' + view) + '?id=' + id + '&pg=' + str(pg))


def likes(request, view, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user)
    else:
        contribution.likes.add(request.user)
    contribution.points = contribution.total_likes()
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view))
    return HttpResponseRedirect(reverse('empo_news:' + view) + '?pg=' + str(pg))


def likes_reply(request, contribution_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    comment.points = comment.total_likes()
    comment.save()
    return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(contribution_id) + '#' + str(comment_id))


def likes_contribution(request, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user)
    else:
        contribution.likes.add(request.user)
    contribution.points = contribution.total_likes()
    contribution.save()
    return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(contribution_id))


def hide(request, view, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.hidden.filter(id=request.user.id).exists():
        contribution.hidden.remove(request.user)
    else:
        contribution.hidden.add(request.user)
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view))
    return HttpResponseRedirect(reverse('empo_news:' + view, args=(pg,)))


def not_implemented(request):
    return HttpResponse('View not yet implemented')


def logout(request):
    do_logout(request)
    return redirect('/')


def users_profile(request, username):
    userFields = UserFields.objects.get(user=User.objects.get(username=username))
    context = {
        "userFields": userFields
    }
    return render(request, 'empo_news/users_profile.html', context)


def profile(request, username):
    userSelected = User.objects.get(username=username)
    if UserFields.objects.filter(user=userSelected).count() == 0:
        userFields = UserFields(user=userSelected, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    else:
        userFields = UserFields.objects.get(user=userSelected)

    if userFields.showdead == 0:
        posS = '0'
    else:
        posS = '1'

    if userFields.noprocrast == 0:
        posN = '0'
    else:
        posN = '1'
    form = UserUpdateForm(
        initial={'email': userSelected.email, 'karma': userFields.karma, 'about': userFields.about,
                 'showdead': posS, 'noprocrast': posN, 'maxvisit': userFields.maxvisit,
                 'minaway': userFields.minaway, 'delay': userFields.delay})

    if userSelected == request.user:
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                UserFields.objects.filter(user=request.user).update(user=request.user, about=form.cleaned_data['about'],
                                                                    showdead=form.cleaned_data['showdead'],
                                                                    noprocrast=form.cleaned_data['noprocrast'],
                                                                    maxvisit=int(form.cleaned_data['maxvisit']),
                                                                    minaway=int(form.cleaned_data['minaway']),
                                                                    delay=int(form.cleaned_data['delay']))
                User.objects.filter(username=request.user.username).update(email=form.cleaned_data['email'])

                return HttpResponseRedirect(reverse('empo_news:user_page', kwargs={"username": userSelected.username}))
    context = {
        "form": form,
        "userSelected": userSelected,
        "userFields": userFields
    }
    return render(request, 'empo_news/profile.html', context)


def increment_comments_number(contrib):
    contrib.comments += 1
    contrib.save()
    if contrib.parent is not None:
        increment_comments_number(contrib.parent)


def item(request):
    contrib_id = int(request.GET.get('id', -1))
    if Comment.objects.filter(id=contrib_id).count() > 0:
        contrib = Comment.objects.get(id=contrib_id)
    else:
        contrib = Contribution.objects.get(id=contrib_id)
    contrib_comments = Comment.objects.filter(contribution_id=contrib_id, parent__isnull=True)\
        .order_by('-publication_time')

    context = {
        "contribution": contrib,
        "comment_form": CommentForm(),
        "contrib_comments": contrib_comments
    }

    if request.method == 'GET':
        try:
            return render(request, 'empo_news/contribution.html', context)
        except Contribution.DoesNotExist:
            return HttpResponse('No such item.')
    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            if contrib.get_class() == "Contribution":
                comment = Comment(user=request.user, contribution=contrib,
                                  publication_time=datetime.today(),
                                  text=comment_form.cleaned_data['comment'])
                comment.save()

                contrib.comments += 1
                contrib.save()
            else:
                comment = Comment(user=request.user, contribution=contrib.contribution, parent=contrib,
                                  publication_time=datetime.today(),
                                  text=comment_form.cleaned_data['comment'])
                comment.save()
                increment_comments_number(contrib)
                contrib.contribution.comments += 1
                contrib.contribution.save()

            return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(contrib_id))
        else:
            return HttpResponseRedirect(reverse('empo_news:addcomment') + '?id=' + str(contrib_id))

    return HttpResponseRedirect(reverse('empo_news:main_page'))


def add_comment(request):
    contrib_id = int(request.GET.get('id', -1))
    contrib = Contribution.objects.get(id=contrib_id)
    context = {
        "contribution": contrib,
        "comment_form": CommentForm()
    }

    if request.method == 'GET':
        try:
            return render(request, 'empo_news/add_comment.html', context)
        except Contribution.DoesNotExist:
            return HttpResponse('No such item.')
    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = Comment(user=request.user, contribution=contrib,
                              publication_time=datetime.today(),
                              text=comment_form.cleaned_data['comment'])
            comment.save()

            contrib.comments += 1
            contrib.save()
            return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(contrib_id))
        else:
            return HttpResponseRedirect(reverse('empo_news:addcomment') + '?id=' + str(contrib_id))

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



def add_reply(request):
    comment_id = int(request.GET.get('id', -1))
    comment = Comment.objects.get(id=comment_id)
    context = {
        "comment": comment,
        "comment_form": CommentForm()
    }

    if request.method == 'GET':
        try:
            return render(request, 'empo_news/add_reply.html', context)
        except Contribution.DoesNotExist:
            return HttpResponse('No such item.')
    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = Comment(user=request.user, contribution=comment.contribution, parent=comment,
                              publication_time=datetime.today(),
                              text=comment_form.cleaned_data['comment'])
            new_comment.save()

            increment_comments_number(comment)
            comment.contribution.comments += 1
            comment.contribution.save()
            return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(new_comment.contribution.id)
                                        + '#' + str(new_comment.parent.id))

    return HttpResponseRedirect(reverse('empo_news:main_page'))


def threads(request, username):
    userSelected = User.objects.get(username=username)
    commentsUser = Comment.objects.filter(user=userSelected)
    context = {
        "userSelected":userSelected,
        "userComments": commentsUser,
    }
    return render(request, 'empo_news/user_comments.html', context)


def delete_comment(request, commentid):
    Comment.objects.filter(id=commentid).delete()
    comments = Comment.objects.filter(user=request.user)
    context = {
        "userSelected":request.user,
        "userComments": comments,
    }
    return render(request, 'empo_news/user_comments.html', context)


def update_comment(request, commentid):
    if request.method == 'POST':
        form = EditCommentForm(request.POST)
        if form.is_valid():
            Comment.objects.filter(id=commentid).update(text=form.cleaned_data['text'])

    comment = Comment.objects.get(id=commentid)
    form = EditCommentForm(
        initial={'text': comment.text})

    context = {
        "comment": comment,
        "form": form,
    }
    return render(request, 'empo_news/edit_comment.html', context)


def comments(request):
    most_recent_list = Comment.objects.all().order_by('-publication_time')[:30]
    more = len(Comment.objects.all()) > 30
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "comments",
        "more": more,
        "next_page": "empo_news:comments_pg",
        "page_value": 1,
        "next_page_value": 2,
        "base_loop_count": 0,
    }
    return render(request, 'empo_news/comments.html', context)


def comments_pg(request, pg):
    if pg <= 1:
        return HttpResponseRedirect(reverse('empo_news:comments'))
    most_recent_list = Comment.objects.all().order_by('-publication_time')[((pg - 1) * 30) + 1:(pg * 30)]
    more = len(Comment.objects.all()) > (pg * 30)
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "comments_pg",
        "more": more,
        "next_page": "empo_news:comments_pg",
        "page_value": pg,
        "next_page_value": pg + 1,
        "base_loop_count": (pg - 1) * 30,
    }
    return render(request, 'empo_news/comments.html', context)

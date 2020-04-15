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
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.filter(comment__isnull=True)
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
        "karma": karma,
    }
    return render(request, 'empo_news/main_page.html', context)


def new_page(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.filter(comment__isnull=True)
    update_show(contributions.order_by('-publication_time'), request.user.id, pg * 30)
    most_recent_list = contributions.filter(show=True).order_by('-publication_time')[list_base:(pg * 30)]
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
        "karma": karma,
    }
    return render(request, 'empo_news/main_page.html', context)


def submitted(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    user_id = request.GET.get('username', "")
    if not User.objects.filter(username=user_id).exists():
        return HttpResponse('No such user')
    base_list = User.objects.get(username=user_id).contribution.filter(comment__isnull=True)

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
        "karma": karma,
    }
    return render(request, 'empo_news/submitted.html', context)


def likes_submit(request, view, id, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if UserFields.objects.filter(user=contribution.user).count() == 0:
        userFields = UserFields(user=contribution.user, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) - 1)
    else:
        contribution.likes.add(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) + 1)
    contribution.points = contribution.total_likes()
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view) + '?id=' + id)
    return HttpResponseRedirect(reverse('empo_news:' + view) + '?id=' + id + '&pg=' + str(pg))


def likes(request, view, pg, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if UserFields.objects.filter(user=contribution.user).count() == 0:
        userFields = UserFields(user=contribution.user, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) - 1)
    else:
        contribution.likes.add(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) + 1)
    contribution.points = contribution.total_likes()
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view))
    return HttpResponseRedirect(reverse('empo_news:' + view) + '?pg=' + str(pg))


def likes_reply(request, contribution_id, comment_id, path):
    comment = get_object_or_404(Comment, id=comment_id)
    if UserFields.objects.filter(user=comment.user).count() == 0:
        userFields = UserFields(user=comment.user, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        UserFields.objects.filter(user=comment.user).update(
            karma=getattr(UserFields.objects.filter(user=comment.user).first(), 'karma', None) - 1)
    else:
        comment.likes.add(request.user)
        UserFields.objects.filter(user=comment.user).update(
            karma=getattr(UserFields.objects.filter(user=comment.user).first(), 'karma', None) + 1)
    comment.points = comment.total_likes()
    comment.save()
    if path == "item":
        return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(contribution_id) + '#' + str(comment_id))
    return HttpResponseRedirect(reverse('empo_news:addreply') + '?id=' + str(comment_id))


def likes_contribution(request, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if UserFields.objects.filter(user=contribution.user).count() == 0:
        userFields = UserFields(user=contribution.user, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) - 1)
    else:
        contribution.likes.add(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) + 1)
    contribution.points = contribution.total_likes()
    contribution.save()
    return HttpResponseRedirect(reverse('empo_news:item') + '?id=' + str(contribution_id))


def likes_comment(request, comment_id, username):
    contribution = get_object_or_404(Contribution, id=comment_id)
    if UserFields.objects.filter(user=contribution.user).count() == 0:
        userFields = UserFields(user=contribution.user, karma=1, about="", showdead=0, noprocrast=0, maxvisit=20,
                                minaway=180, delay=0)
        userFields.save()
    if contribution.likes.filter(id=request.user.id).exists():
        contribution.likes.remove(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) - 1)
    else:
        contribution.likes.add(request.user)
        UserFields.objects.filter(user=contribution.user).update(
            karma=getattr(UserFields.objects.filter(user=contribution.user).first(), 'karma', None) + 1)
    contribution.points = contribution.total_likes()
    contribution.save()
    return HttpResponseRedirect(reverse('empo_news:threads', kwargs={'username': username}))


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


def hide_no_page(request, view, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.hidden.filter(id=request.user.id).exists():
        contribution.hidden.remove(request.user)
    else:
        contribution.hidden.add(request.user)
    contribution.save()
    return HttpResponseRedirect(reverse('empo_news:' + view) + "?id=" + str(contribution_id))


def not_implemented(request):
    return HttpResponse('View not yet implemented')


def logout(request):
    do_logout(request)
    return redirect('/')


def profile(request, username):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
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
        "userFields": userFields,
        "karma": karma,
        "notBottom": True,
    }
    return render(request, 'empo_news/profile.html', context)


def increment_comments_number(contrib):
    contrib.comments += 1
    contrib.save()
    if contrib.parent is not None:
        increment_comments_number(contrib.parent)


def item(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    contrib_id = int(request.GET.get('id', -1))
    if Comment.objects.filter(id=contrib_id).count() > 0:
        contrib = Comment.objects.get(id=contrib_id)
    else:
        contrib = Contribution.objects.get(id=contrib_id)
    contrib_comments = Comment.objects.filter(contribution_id=contrib_id, parent__isnull=True) \
        .order_by('-publication_time')

    context = {
        "contribution": contrib,
        "comment_form": CommentForm(),
        "contrib_comments": contrib_comments,
        "karma": karma,
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
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    contrib_id = int(request.GET.get('id', -1))
    contrib = Contribution.objects.get(id=contrib_id)
    context = {
        "contribution": contrib,
        "comment_form": CommentForm(),
        "karma": karma,
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
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    comment_id = int(request.GET.get('id', -1))
    comment = Comment.objects.get(id=comment_id)
    context = {
        "comment": comment,
        "comment_form": CommentForm(),
        "karma": karma,
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
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    userFields = UserFields.objects.filter(user=request.user)
    userSelected = User.objects.get(username=username)
    commentsUser = Comment.objects.filter(user=userSelected)
    context = {
        "userSelected": userSelected,
        "userComments": commentsUser,
        "userFields": userFields,
        "karma": karma,
        "highlight": "user_comments",
    }
    return render(request, 'empo_news/user_comments.html', context)


def delete_comment(request, commentid):
    Comment.objects.filter(id=commentid).delete()
    comments = Comment.objects.filter(user=request.user)
    context = {
        "userSelected": request.user,
        "userComments": comments,
        "highlight": "user_comments",
    }
    return render(request, 'empo_news/user_comments.html', context)


def update_comment(request, commentid):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
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
        "karma": karma,
    }
    return render(request, 'empo_news/edit_comment.html', context)


def comments(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    most_recent_list = Comment.objects.all().order_by('-publication_time')[list_base:(pg * 30)]
    more = len(Comment.objects.all()) > (pg * 30)
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "comments",
        "highlight": "comments",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
        "karma": karma,
    }
    return render(request, 'empo_news/comments.html', context)


def ask_list(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.filter(comment__isnull=True, url__isnull=True)
    update_show(contributions.order_by('-points'), request.user.id, pg * 30)
    most_points_list = contributions.filter(show=True).order_by('-points')[list_base:(pg * 30)]
    more = len(contributions.filter(show=True)) > (pg * 30)
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "ask_list",
        "highlight": "ask",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
        "karma": karma,
    }
    return render(request, 'empo_news/main_page.html', context)


def show_list(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.filter(comment__isnull=True, url__isnull=True, title__startswith='Show EN: ')
    update_show(contributions.order_by('-points'), request.user.id, pg * 30)
    most_points_list = contributions.filter(show=True).order_by('-points')[list_base:(pg * 30)]
    more = len(contributions.filter(show=True)) > (pg * 30)
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "show_list",
        "highlight": "show",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
        "karma": karma,
    }
    return render(request, 'empo_news/main_page.html', context)


def update_show_hidden(all_contributions, userid, border):
    count_shown = 0
    i = 0
    length = len(all_contributions)
    while count_shown < border and i < length:
        contribution = all_contributions[i]
        if contribution.hidden.filter(id=userid).exists():
            contribution.show = True
            count_shown += 1
        else:
            contribution.show = False
        contribution.save()
        i += 1


def hidden(request, userid):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    selectedUser = User.objects.filter(id=userid).first()
    contributions = Contribution.objects.filter(comment__isnull=True)
    update_show_hidden(contributions.order_by('-points'), userid, pg * 30)
    most_points_list = contributions.filter(show=True).order_by('-points')[list_base:(pg * 30)]
    more = len(contributions.filter(show=True)) > (pg * 30)
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "hidden",
        "highlight": "hidden",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
        "karma": karma,
        "selectedUser": selectedUser,
    }
    return render(request, 'empo_news/main_page.html', context)


def unhide(request, view, pg, contribution_id, userid):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if contribution.hidden.filter(id=request.user.id).exists():
        contribution.hidden.remove(request.user)
    else:
        contribution.hidden.add(request.user)
    contribution.save()
    if pg == 1:
        return HttpResponseRedirect(reverse('empo_news:' + view, kwargs={'userid': userid}))
    return HttpResponseRedirect(reverse('empo_news:' + view, args=(pg,), kwargs={'userid': userid}, ))


def voted_submissions(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    contributions = Contribution.objects.filter(comment__isnull=True,
                                                likes__username__contains=request.user.username).exclude(
        user=request.user)
    update_show(contributions.order_by('-points'), request.user.id, pg * 30)
    most_points_list = contributions.filter(show=True).order_by('-points')[list_base:(pg * 30)]
    more = len(contributions.filter(show=True)) > (pg * 30)
    for contribution in most_points_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_points_list,
        "user": request.user,
        "path": "voted_submissions",
        "highlight": "voted_submissions",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
        "karma": karma,
    }
    return render(request, 'empo_news/main_page.html', context)


def voted_comments(request):
    karma = 0
    if request.user.is_authenticated:
        karma = getattr(UserFields.objects.filter(user=request.user).first(), 'karma', None)
    pg = int(request.GET.get('pg', 1))
    base_path = request.get_full_path().split('?')[0]
    list_base = ((pg - 1) * 30) + 1
    if pg < 1:
        return HttpResponseRedirect(base_path)
    elif pg == 1:
        list_base = 0

    comments = Comment.objects.filter(likes__username__contains=request.user.username).exclude(user=request.user)
    most_recent_list = comments.order_by('-publication_time')[list_base:(pg * 30)]
    more = len(comments) > (pg * 30)
    for contribution in most_recent_list:
        contribution.liked = not contribution.likes.filter(id=request.user.id).exists()
        contribution.save()
    context = {
        "list": most_recent_list,
        "user": request.user,
        "path": "voted_comments",
        "highlight": "voted_comments",
        "more": more,
        "next_page": base_path + "?pg=" + str(pg + 1),
        "page_value": pg,
        "base_loop_count": (pg - 1) * 30,
        "karma": karma,
    }
    return render(request, 'empo_news/comments.html', context)

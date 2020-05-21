from django import template

register = template.Library()


@register.filter
def get_class(contribution):
    return contribution.get_type()


@register.filter
def get_type(contribution):
    return contribution.get_class()


@register.filter
def short_text(contribution):
    return short_text_format(str(contribution.text))


@register.filter
def short_title(contribution):
    return short_text_format(str(contribution.title))


def short_text_format(text):
    if len(text) > 80:
        next_space = text.index(" ", 79)
        return text[:next_space] + "..."
    return text


@register.filter
def is_liked(contribution):
    return contribution.is_liked()


@register.filter
def is_contribution_liked(contribution, user_id):
    return contribution.user_likes.filter(id=user_id).exists()
  

@register.filter
def all_replies(comment):
    return comment.comment_set.all().order_by('-publication_time')


@register.filter
def is_hidden(contribution, user_id):
    return contribution.user_id_hidden.filter(id=user_id).exists()

@register.filter
def google_url(originalString):
    return originalString.replace(" ", "+")

@register.filter
def get_domain(url):
    url_split = url.split('/')
    if len(url_split) > 2:
        return url_split[2]
    return url

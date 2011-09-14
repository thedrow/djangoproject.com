
import datetime

from django.conf import settings
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseBadRequest
from django.core.paginator import Paginator, InvalidPage

from haystack.query import SearchQuerySet
from haystack.forms import ModelSearchForm

from django_website.logger.models import Channel, Message
from django_website.logger.forms import NonEmptyModelSearchForm


@never_cache
def channel_detail(request, channel_name, template="logger/channel_detail.html",
        load_all=True, form_class=ModelSearchForm,
        extra_context=None):
    channel = get_object_or_404(Channel, name="#%s" % channel_name)
    query = ''
    results = SearchQuerySet().models(Message).order_by("logged").filter(channel_id=channel.pk)

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=results, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=results, load_all=load_all)

    paginator = Paginator(results, settings.LOGGER_PAGINATE_BY)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
        'channel': channel,
        'channel_name': channel_name,  # used for {% url %}
        'date': datetime.datetime.today(),
    }

    if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render(request, template, context)


def channel_detail_day(request, channel_name, year, month, day, page=None):
    channel = get_object_or_404(Channel, name="#%s" % channel_name)
    ctx = {}
    date = datetime.date(*map(int, (year, month, day)))
    # check if the date is today, if True then dont allow caching.
    if date == datetime.date.today():
        ctx.update({"today": True})
    paginator = Paginator(channel.message_set.filter(
        logged__range=(date, date + datetime.timedelta(days=1)),
    ).order_by("logged"), settings.LOGGER_PAGINATE_BY)
    if page is None:
        page_number = paginator.num_pages
    else:
        try:
            page_number = int(page)
        except ValueError:
            return HttpResponseBadRequest()
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404
    return render(request, "logger/channel_detail_day.html", dict(ctx, **{
        "channel": channel,
        "channel_name": channel_name,  # used for {% url %}
        "date": date,
        "paginator": paginator,
        "is_paginated": paginator.count >= settings.LOGGER_PAGINATE_BY,
        "page_number": page_number,
        "page": page,
        "messages": page.object_list,
    }))

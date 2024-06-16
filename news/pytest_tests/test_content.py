import pytest
from http import HTTPStatus

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_homepage_news_count_and_order(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    object_list = list(response.context['object_list'])
    assert len(object_list) <= settings.NEWS_COUNT_ON_HOME_PAGE
    sorted_list = sorted(object_list, key=lambda x: x.date, reverse=True)
    assert object_list == sorted_list



def test_comments_order(client, news, comments_list):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.get(url)
    news = response.context['news']
    all_comment = list(news.comment_set.all())
    assert all_comment == sorted(all_comment, key= lambda x: x.created)


def test_client_and_anonymous_has_form(client, news, admin_client):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.get(url)
    admin_response = admin_client.get(url)
    assert (
        isinstance(admin_response.context['form'], CommentForm)
        and 'form' not in response.context
    )
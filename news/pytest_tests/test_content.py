import pytest

from django.conf import settings

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_homepage_news_count_and_order(client, news_list, home_url):
    response = client.get(home_url)
    object_list = list(response.context['object_list'])
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE
    sorted_list = sorted(object_list, key=lambda x: x.date, reverse=True)
    assert object_list == sorted_list


def test_comments_order(client, news, comments_list, detail_url):
    response = client.get(detail_url)
    news = response.context['news']
    all_comment = list(news.comment_set.all())
    assert all_comment == sorted(all_comment, key=lambda x: x.created)


def test_authorized_user_has_form(admin_client, news, detail_url):
    admin_response = admin_client.get(detail_url)
    assert isinstance(admin_response.context['form'], CommentForm)


def test_anonymous_user_has_no_form(client, news, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context

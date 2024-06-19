from datetime import timedelta

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

import pytest


TITLE = 'Заголовок'
TEXT = 'Текст новости'
COMMENT_TEXT = 'Текст комментария'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title=TITLE,
        text=TEXT
    )
    return news


@pytest.fixture
def news_list():
    news_items = []
    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_date = timezone.now() - timedelta(days=i)
        news_item = News.objects.create(
            title=TITLE + str(i),
            text=TEXT + str(i),
            date=news_date
        )
        news_items.append(news_item)
    return news_items


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT,
    )
    return comment


@pytest.fixture
def comments_list(news, author):
    for i in range(5):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'{COMMENT_TEXT} {i}',
            created=timezone.now() + timedelta(days=i)
        )
        comment.save()
    return comments_list


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', kwargs={'pk': news.pk})


@pytest.fixture
def edit_url(news):
    return reverse('news:edit', kwargs={'pk': news.pk})


@pytest.fixture
def delete_url(news):
    return reverse('news:delete', kwargs={'pk': news.pk})


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')

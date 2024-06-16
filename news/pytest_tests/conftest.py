import pytest
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


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
        title='Новость',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_list():
    news_items = []
    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_date = timezone.now() - timedelta(days=i)
        news_item = News.objects.create(
            title='Новость' + str(i),
            text='Текст новости' + str(i),
            date=news_date
        )
        news_items.append(news_item)
    return news_items


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def comments_list(news, author):
    for i in range(5):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Комментарий {i}',
            created=timezone.now() + timedelta(days=i)
        )
        comment.save()
    return comments_list
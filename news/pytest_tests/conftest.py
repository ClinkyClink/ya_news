import pytest
from pytest_lazyfixture import lazy_fixture
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.test.client import Client

from news.models import News, Comment


PK = 1
AUTHOR_NAME = 'Автор'
USER_NAME = 'Пользователь'
TITLE = 'Заголовок'
TEXT = 'Текст новости'
COMMENT_TEXT = 'Текст комментария'
ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username=AUTHOR_NAME)


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username=USER_NAME)


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


class URL_NAME:
    def __init__(self, home, detail, edit, delete, login, logout, signup):
        self.home = home
        self.detail = detail
        self.edit = edit
        self.delete = delete
        self.login = login
        self.logout = logout
        self.signup = signup

URL = URL_NAME(
    reverse('news:home'),
    reverse('news:detail', args=(PK,)),
    reverse('news:edit', args=(PK,)),
    reverse('news:delete', args=(PK,)),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)
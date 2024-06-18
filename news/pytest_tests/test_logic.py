import pytest
from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects
from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING
from .conftest import URL


FORM_DATA = {
    'text': 'Новый текст комментария',
}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    initial_count = Comment.objects.count()
    client.post(URL.detail, data=FORM_DATA)
    comment_count = Comment.objects.count()
    assert initial_count == comment_count


def test_user_can_create_comment(author_client, author, news):
    expected_count = Comment.objects.count() + 1
    response = author_client.post(URL.detail, data=FORM_DATA)
    comments_count = Comment.objects.count()
    new_comment = Comment.objects.get()
    assert expected_count == comments_count
    assert all(
        (
            new_comment.text == FORM_DATA['text'],
            new_comment.author == author,
            new_comment.news == news,
        )
    )


@pytest.mark.parametrize('word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, news, word):
    initial_count = Comment.objects.count()
    text_with_bad_words = {'text': f'Вы все {word}'}
    response = author_client.post(URL.detail, data=text_with_bad_words)
    comment_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert initial_count == comment_count


def test_author_can_delete_comment(author_client, comment, news):
    expected_count = Comment.objects.count() - 1
    response = author_client.delete(URL.delete)
    comment_count = Comment.objects.count()
    assertRedirects(response, f'{URL.detail}#comments')
    assert expected_count == comment_count


def test_author_can_edit_comment(author_client, author, comment, news):
    expected_count = Comment.objects.count()
    response = author_client.post(URL.edit, data=FORM_DATA)
    assertRedirects(response, f'{URL.detail}#comments')
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert expected_count == comments_count
    assert all((comment.text == 'Новый текст комментария', comment.author == author))


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    expected_count = Comment.objects.count()
    response = admin_client.delete(URL.delete)
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count


def test_user_cant_edit_comment_of_another_user(author, admin_client, comment):
    expected_count = Comment.objects.count()
    response = admin_client.post(URL.edit, data=FORM_DATA)
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count
    assert all((comment.text == 'Текст комментария', comment.author == author))
import pytest
from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


FORM_DATA = {
    'text': 'Новый текст комментария',
}
DETAIL_URL = pytest.lazy_fixture('detail_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, detail_url):
    initial_count = Comment.objects.count()
    client.post(detail_url, data=FORM_DATA)
    comment_count = Comment.objects.count()
    assert initial_count == comment_count


def test_user_can_create_comment(author_client, author, news, detail_url):
    expected_count = Comment.objects.count() + 1
    author_client.post(detail_url, data=FORM_DATA)
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
def test_user_cant_use_bad_words(author_client, news, word, detail_url):
    initial_count = Comment.objects.count()
    text_with_bad_words = {'text': f'Вы все {word}'}
    response = author_client.post(detail_url, data=text_with_bad_words)
    comment_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert initial_count == comment_count


def test_author_can_delete_comment(author_client,
                                   comment,
                                   news,
                                   delete_url,
                                   detail_url):
    expected_count = Comment.objects.count() - 1
    response = author_client.delete(delete_url)
    comment_count = Comment.objects.count()
    assertRedirects(response, f"{detail_url}#comments")
    assert expected_count == comment_count


def test_author_can_edit_comment(author_client,
                                 author,
                                 comment,
                                 news,
                                 edit_url,
                                 detail_url):
    expected_count = Comment.objects.count()
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, f"{detail_url}#comments")
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert expected_count == comments_count
    assert all((comment.text == 'Новый текст комментария',
                comment.author == author))


def test_user_cant_delete_comment_of_another_user(admin_client,
                                                  comment,
                                                  delete_url):
    expected_count = Comment.objects.count()
    response = admin_client.delete(delete_url)
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count


def test_user_cant_edit_comment_of_another_user(author,
                                                admin_client,
                                                comment,
                                                edit_url):
    expected_count = Comment.objects.count()
    response = admin_client.post(edit_url, data=FORM_DATA)
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count
    assert all((comment.text == 'Текст комментария', comment.author == author))

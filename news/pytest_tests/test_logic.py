import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, comment):
    url = reverse('news:detail', kwargs={'pk': comment.pk})
    response = client.post(url, data=comment)
    assert Comment.objects.count() == 0

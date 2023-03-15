import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_tos_import_permissions(client, user):
    url = reverse("admin:import-tos")
    login_url = reverse("admin:login")

    response = client.post(url)
    assert response.status_code == 302
    assert response["Location"].startswith(login_url)

    client.force_login(user)
    response = client.post(url)
    assert response.status_code == 302
    assert response["Location"].startswith(login_url)

    user.is_staff = True
    user.save()
    response = client.post(url)
    assert response.status_code == 403

    user.is_superuser = True
    user.save()
    client.force_login(user)
    response = client.post(url)
    assert response.status_code == 200

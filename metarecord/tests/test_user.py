import json

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse

User = get_user_model()

LIST_URL = reverse("user-list")


def get_detail_url(user):
    return reverse("user-detail", kwargs={"uuid": user.uuid})


def _check_user_object_matches_data(user_obj, data, permissions=None):
    assert set(data.keys()) == {
        "uuid",
        "first_name",
        "last_name",
        "username",
        "permissions",
    }

    assert data["uuid"] == str(user_obj.uuid)
    assert data["first_name"] == user_obj.first_name
    assert data["last_name"] == user_obj.last_name
    assert data["username"] == user_obj.username

    permissions = permissions or set()
    assert set(data["permissions"]) == permissions


@pytest.mark.django_db
def test_permissions_exist():
    for perm in ("can_edit", "can_approve", "can_review"):
        assert Permission.objects.filter(codename=perm).exists()


@pytest.mark.django_db
def test_user_endpoint_requires_authentication(api_client, user):
    response = api_client.get(LIST_URL)
    assert response.status_code == 401

    response = api_client.get(get_detail_url(user))
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_list_endpoint(user, user_2, user_api_client):
    perm = Permission.objects.get(codename="can_edit")
    user.user_permissions.add(perm)

    response = user_api_client.get(LIST_URL)
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1

    user.refresh_from_db()
    _check_user_object_matches_data(user, results[0], {"can_edit"})


@pytest.mark.django_db
def test_user_detail_endpoint(user, user_2, user_api_client):
    perms = Permission.objects.filter(codename__in=("can_edit", "can_approve"))
    for perm in perms:
        user.user_permissions.add(perm)

    response = user_api_client.get(get_detail_url(user))
    assert response.status_code == 200

    user.refresh_from_db()
    _check_user_object_matches_data(user, response.data, {"can_edit", "can_approve"})


@pytest.mark.django_db
def test_cannot_see_other_user_data(user, user_2, user_api_client):
    response = user_api_client.get(get_detail_url(user_2))
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_permission_list(user, user_api_client):
    permissions = Permission.objects.filter(
        codename__in=("can_view_modified_by", "add_bulkupdate", "approve_bulkupdate")
    )
    user.user_permissions.add(*permissions)

    response = user_api_client.get(get_detail_url(user))
    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert response_data["permissions"] == [
        "can_view_modified_by",
        "add_bulkupdate",
        "approve_bulkupdate",
    ]

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


@pytest.mark.parametrize(
    "username,password,email",
    [
        ("admin", "password", "admin@example.com"),
        ("super", "secret", "email@example.com"),
    ],
)
@pytest.mark.django_db
def test_add_admin_user_creates(username, password, email):
    call_command("add_admin_user", username=username, password=password, email=email)

    user = User.objects.first()
    assert user.username == username
    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
def test_add_admin_user_random_password():
    """Test that the command generates a random password if none is given."""
    assert User.objects.count() == 0
    call_command("add_admin_user")

    user = User.objects.first()
    assert user.username == "admin"
    assert user.email == "admin@example.com"
    assert user.has_usable_password()
    assert not user.check_password("admin")

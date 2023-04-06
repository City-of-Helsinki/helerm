from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Add admin user"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--username", type=str, help="Username", default="admin"
        )
        parser.add_argument("-p", "--password", type=str, help="Password", default="")
        parser.add_argument(
            "-e", "--email", type=str, help="Email", default="admin@example.com"
        )

    def handle(self, *args, **kwargs):
        if not get_user_model().objects.filter(username=kwargs["username"]).count():
            password = kwargs["password"]
            if not password:
                password = get_random_string(20)
                self.stdout.write(
                    self.style.WARNING(f"Generated admin password {password}")
                )
                self.stdout.write(
                    self.style.WARNING("You should probably go and change it.")
                )

            get_user_model().objects.create_superuser(
                kwargs["username"], kwargs["email"], password
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created admin user {kwargs['username']}")
            )
        else:
            self.stdout.write(
                f"Admin user {kwargs['username']} already exists, no need to create."
            )

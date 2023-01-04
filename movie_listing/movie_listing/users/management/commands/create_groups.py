from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand

from ....movies.models import Movie
from ....sources.models import Source


class Command(BaseCommand):
    help = 'Creates customer group for users and add permissions'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.groups = [
            {
                "name": "staff",
                "allowed_actions": [
                    "add_source",
                    "change_source",
                    "delete_source",
                    "view_source",

                    "add_movie",
                    "change_movie",
                    "delete_movie",
                    "view_movie",
                ]
            },
            {
                "name": "customers",
                "allowed_actions": [
                    "add_movie",
                    "delete_movie"
                ]
            },
        ]

    @property
    def permissions(self):
        content_type = ContentType.objects.get_for_model(Source)
        source_permissions = Permission.objects.filter(content_type=content_type)

        content_type = ContentType.objects.get_for_model(Movie)
        movie_permissions = Permission.objects.filter(content_type=content_type)

        return source_permissions.union(movie_permissions)

    def add_permissions_to_group(self, group, allowed_actions):
        for permission in self.permissions:
            if permission.codename in allowed_actions:
                group.permissions.add(permission)
                print(f"Permission {permission.codename} add to Group {str(group)}")

    def handle(self, *args, **options):
        for group in self.groups:
            new_group, created = Group.objects.get_or_create(name=group['name'])
            if created:
                print(f"Group {str(new_group)} was created.")

                if group.get('allowed_actions'):
                    self.add_permissions_to_group(new_group, group['allowed_actions'])

            else:
                print(f"Group {str(new_group)} already exists.")

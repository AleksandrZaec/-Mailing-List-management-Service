from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from mailing.models import Mailing
from users.models import User

content_type_1 = ContentType.objects.get_for_model(Mailing)
mailing_permissions = [
    'view_sending',
    'set_active',
]
content_type_2 = ContentType.objects.get_for_model(User)
user_permissions = [
    'view_user',
    'set_active',
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        managers_group = Group.objects.create(name='managers')
        for p in mailing_permissions:
            perm = Permission.objects.get(codename=p, content_type=content_type_1)
            managers_group.permissions.add(perm)
        for p in user_permissions:
            perm = Permission.objects.get(codename=p, content_type=content_type_2)
            managers_group.permissions.add(perm)
        managers_group.save()
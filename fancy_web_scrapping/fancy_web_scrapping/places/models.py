from django.db.models import Model, DateTimeField, CharField, URLField
from django.utils.translation import gettext as _


class Place(Model):
    created_at = DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = DateTimeField(_("Updated At"), auto_now=True)
    name = CharField(_("Name"), max_length=140,
                     unique=True, blank=False, null=False)
    address = CharField(_("Address"), max_length=255, blank=False, null=True)
    url = URLField(_("URL"), max_length=200, blank=False, null=True)

    def __str__(self):
        return self.name

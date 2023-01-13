from django.db.models import Model, CharField, URLField
from django.utils.translation import gettext as _


class Place(Model):
    name = CharField(_("Name"), max_length=140, blank=False, null=False)
    address = CharField(_("Address"), max_length=255, blank=False, null=True)
    url = URLField(_("URL"), max_length=200, blank=False, null=True)

    def __str__(self):
        return self.name

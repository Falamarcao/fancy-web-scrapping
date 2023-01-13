from django.db.models import Model, CharField, URLField, PositiveIntegerField
from django.utils.translation import gettext as _


class Source(Model):
    name = CharField(_("Name"), max_length=140, blank=True, null=False)
    url = URLField(_("URL"), max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Source {self.pk}"
        super(Source, self).save(*args, **kwargs)

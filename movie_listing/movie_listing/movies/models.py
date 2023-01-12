from django.db.models import (Model, DateTimeField, CharField, ForeignKey,
                              URLField, JSONField, CASCADE, PROTECT)
from django.utils.translation import gettext as _
from ..sources.models import Source
from ..places.models import Place


class Movie(Model):
    source = ForeignKey(
        Source,
        verbose_name=_("Source"),
        blank=False,
        null=True,
        on_delete=CASCADE,
        related_name='source_movie'
    )
    
    place = ForeignKey(
        Place,
        verbose_name=_("Place"),
        blank=False,
        null=True,
        on_delete=CASCADE,
        related_name='place_movie'
    )
    
    image_url = URLField(_("Image URL"), max_length=200)
    
    name = CharField(_("Name"), max_length=140, blank=False, null=False)
    description = CharField(_("Description"), max_length=140, blank=False, null=False)
    duration = CharField(_("Duration"), max_length=10, blank=False, null=False)
    
    sessions = JSONField(_("Sessions"), blank=False, null=True) # e.g. {"3D": ["20:30", "21:30"]}

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ('source', 'place', 'name',),
        )
        # constraints = [
        #     CheckConstraint(
        #         check=Q(end_at__gt=F('start_at')),
        #         name='check_start_date',
        #     ),
        # ]

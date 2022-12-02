# Django
from django.db import models

class DateBaseModel(models.Model):

    """ API Date Base Model

    DateBaseModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides every
    table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + updated (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text="Date time on which the object was created."
    )
    updated = models.DateTimeField(
        'updated at',
        auto_now=True,
        help_text="Date time on wich the object was last updated."
    )

    class Meta:
        """Meta options."""
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-updated']
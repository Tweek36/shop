from typing import Any
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# class UnicodeProductNameValidator(validators.RegexValidator):
#    regex = r"^[A-Za-z0-9\-\s\[\]\(\)_]+$"
#    message = _(
#        "^[A-Za-z0-9\-\s\[\]\(\)]+$"
#    )
#    flags = 0
#
# class UnicodeProductValueValidator(validators.RegexValidator):
#    regex = r"^[A-Za-z0-9!@~#$%^&*()\-_=+\[\]\{\}.,<>\?/|:;\"'^\\\s]+$"
#    message = _(
#        "Enter a valid name."
#    )
#    flags = 0


class Product(models.Model):
    # product_validator = UnicodeProductNameValidator()
    # product_value_validator = UnicodeProductValueValidator()
    TYPE_CHOICES = [
        ("cpu", "CPU"),
    ]

    name = models.CharField(
        _("name"),
        max_length=127,
        unique=True,
        help_text=_("Required. 128 characters or fewer."),
        # validators=[product_validator],
        error_messages={
            "unique": _("A product with that name already exists."),
        },
    )

    url = models.CharField(_("url"), max_length=127, unique=True, blank=True)

    type = models.CharField(_("type"), max_length=127, choices=TYPE_CHOICES)

    propertys = models.JSONField(
        _("propertys"),
    )

    img = models.ImageField(
        _("img"),
        upload_to="img",
        default="img/default.jpg",
    )

    coment = models.TextField(
        _("coment"),
        max_length=511,
        unique=False,
        help_text=_("Required. 511 characters or fewer."),
        # validators=[product_value_validator],
        blank=True,
    )

    amount = models.PositiveSmallIntegerField(
        _("amount"), help_text=_("Required. Positive number."), default=0
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.url == "":
            self.url = (
                self.name.replace(" ", "-")
                .replace("_", "-")
                .translate(str.maketrans("", "", "()[]/\|/*+&?,.!<>^$#@`'\";:~=%"))
            )
        if self.url in ["create"]:
            raise Exception("Invalid name or url.")
        super().save(*args, **kwargs)

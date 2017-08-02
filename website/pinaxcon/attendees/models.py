# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Attendee(models.Model):
    user = models.OneToOneField(User, related_name="attendee", verbose_name=_("User"))
    full_name = models.CharField(verbose_name="Nombre completo o nick", max_length=100,
                            help_text=(u"Como te gustaría que se imprima en tu"
                                        " gafete.(si querés puede ser un nick)"))
    annotation = models.TextField(verbose_name="Observaciones",
                                  help_text=("Si tenés alguna necesidad "
                                  "particular que necesites que contemplemos "
                                  "para el evento contanos y haremos lo posible "
                                  "por ayudarte. "
                                  "Te recomendamos reservar tu vianda para los "
                                  "días sábado y domingo, ya que cerca del "
                                  "complejo las ofertas gastronómicas son "
                                  "reducidas Podrás elegir el tipo de vianda de "
                                  "acuerdo a tus necesidades. Encontrarás el "
                                  "link para hacerlo al confirmar la "
                                  "registración."),
                                  blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True,
        editable=False)
    cv = models.FileField(upload_to="attendees_cvs", blank=True,
            verbose_name="Curriculum vitae")
    show_to_sponsor = models.BooleanField(verbose_name="Compartir mis datos "
                                          "personales", help_text=("Acepto que mis datos "
        "personales se compartan con los sponsors"))
    is_vegetarian = models.BooleanField(default=False)
    is_tacc = models.BooleanField(default=False)
    meal_on_saturday = models.IntegerField(blank=True, null=True)
    meal_on_sunday = models.IntegerField(blank=True, null=True)
    tshirt_male_s = models.IntegerField(blank=True, null=True)
    tshirt_male_m = models.IntegerField(blank=True, null=True)
    tshirt_male_l = models.IntegerField(blank=True, null=True)
    tshirt_male_xl = models.IntegerField(blank=True, null=True)
    tshirt_male_xxl = models.IntegerField(blank=True, null=True)
    tshirt_male_xxxl = models.IntegerField(blank=True, null=True)
    tshirt_male_xxxxl = models.IntegerField(blank=True, null=True)
    tshirt_female_s = models.IntegerField(blank=True, null=True)
    tshirt_female_m = models.IntegerField(blank=True, null=True)
    tshirt_female_l = models.IntegerField(blank=True, null=True)
    tshirt_female_xl = models.IntegerField(blank=True, null=True)
    is_acredited = models.BooleanField(default=False)
    amount_to_pay = models.IntegerField(default=0)
    require_certificate = models.BooleanField(default=False)
    wanna_party = models.BooleanField(default=False)

    class Meta:
        ordering = ['full_name']
        verbose_name = "Asistente"
        verbose_name_plural = "Asistentes"

    def __str__(self):
        if self.user:
            return self.full_name
        else:
            return "?"

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from jedzonko.models import Recipe


def populate(apps, schema_editor):
    Recipe.objects.create(name="Szybka sałatka z chilli.", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, chilli.", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp chilli.", preparation_time=15)
    Recipe.objects.create(name="Szybka sałatka z pietruszką", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, pietruszka", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp pietruszką", preparation_time=12)
    Recipe.objects.create(name="Szybka sałatka z mango", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, mango", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp mango", preparation_time=14)
    Recipe.objects.create(name="Szybka sałatka z parmezanem", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, parmezanem", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp parmezanem", preparation_time=15)
    Recipe.objects.create(name="Szybka sałatka z owsem", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, owies", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp owsem", preparation_time=16)
    Recipe.objects.create(name="Szybka sałatka z żytem", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, żyto", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp żytem", preparation_time=17)
    Recipe.objects.create(name="Szybka sałatka z wakame", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, wakame", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp wakame", preparation_time=11)
    Recipe.objects.create(name="Szybka sałatka z kimchi", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, kimchi", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp kimchi", preparation_time=10)
    Recipe.objects.create(name="Szybka sałatka z edamame", ingredients="Sałata lodowa, kilka plastrów kaszanki, masło, czosnek, edamame", description="Sałatę porwij na kawałeczki, podsmaż kaszankę na odrobinie masła, dopraw solą, pieprzem i czosnkiem. Na koniec posyp edamame", preparation_time=14)


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0002_recipe_instructions'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]

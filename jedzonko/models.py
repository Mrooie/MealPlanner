from django.db import models
# Enum -  dostępne w całym projekcie zastępstwo choices i modelu dayname
from enum import Enum


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    instructions = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    preparation_time = models.SmallIntegerField()
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='recipeplan')


# Enum zastępuje model dayname w projekcie. Ściągawka: http://tiny.cc/17bmez
class WeekDays(Enum):  # Zamiast choices dla dni tygodnia.
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    day_name = models.SmallIntegerField(choices=[(tag.name, tag.value) for tag in WeekDays])


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255)

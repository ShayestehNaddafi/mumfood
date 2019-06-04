from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    vegan = models.BooleanField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    like_number = models.IntegerField(default= 0)
    ingredients = models.ManyToManyField(Ingredient)
    vegan = models.BooleanField()

    def __str__(self):
        return self.name




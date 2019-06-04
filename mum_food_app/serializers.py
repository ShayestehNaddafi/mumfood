from rest_framework import serializers
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe_ingredients = IngredientSerializer(source ='ingredients', many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'like_number', 'recipe_ingredients', 'vegan')



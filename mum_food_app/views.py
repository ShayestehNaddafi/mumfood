from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe,Ingredient
from .serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer


class RecipeListByPopularityView(APIView):

    def get(self, request):
        try:
            all_recipes = Recipe.objects.all().order_by('-like_number')
            recipes_serialized = RecipeIngredientSerializer(all_recipes, many=True)
            response_data = {'status': 'success',
                             'data': recipes_serialized.data}

        except Exception as error:
            error = 'Request Failed {0}'.format(error)
            response_data = {'status': 'failed',
                             'errors': error}
        return Response(response_data)

    def post(self, request):
        items = request.data['ingredients']
        params = request.data['params']
        ingredients = []
        vegan = []
        for ingredient in items:
            ing = Ingredient.objects.get(name=ingredient)
            ingredients.append(ing.id)
            vegan.append(ing.vegan)
        params['ingredients'] = ingredients
        params['vegan'] = all(vegan)
        recipe_serialized = RecipeSerializer(data=params)
        if recipe_serialized.is_valid():
            recipe = recipe_serialized.save()
            return Response({'status': 'success',
                             'data': recipe.name})
        return Response({'status': 'failed',
                         'data': recipe_serialized.errors})


class IngredientView(APIView):
    def get(self, request):
        try:
            all_ingredients = Recipe.objects.all()
            serializer = IngredientSerializer(all_ingredients, many=True)
            response_data = {'status': 'success',
                             'data': serializer.data}

        except Exception as error:
            error = 'Request Failed {0}'.format(error)
            response_data = {'status': 'failed',
                             'errors': error}
        return Response(response_data)

    def post(self, request):
        ingredient = IngredientSerializer(request.data)
        if recipe_serialized.is_valid():
            recipe = ingredient.save()
            return Response({
                    'status': 'success',
                    'data': recipe.name})
        return Response({
            'status': 'failed',
            'data': ingredient.errors})


class RecipeView(APIView):
    def get(selfs, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            recipe_serialized = RecipeIngredientSerializer(recipe)
            response_data = {'status': 'success',
                             'data': recipe_serialized.data}

        except Exception as error:
            error= 'Request Failed {0}'.format(error)
            response_data = {'status': 'failed',
                             'errors': error}
        return Response(response_data)

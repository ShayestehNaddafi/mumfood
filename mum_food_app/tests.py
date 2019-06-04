from django.test import TestCase, Client
from mum_food_app.models import Recipe, Ingredient


class MumFoodGetApisTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(MumFoodGetApisTests, cls).setUpClass()
        recipe_1 = Recipe.objects.create(name='veg_pizza',
                                         description='This is a recipe of a vegan pizza',
                                         like_number='20',
                                         vegan=True)
        recipe_2 = Recipe.objects.create(name='meat_pizza',
                                         description='This is a recipe of a all meat pizza',
                                         like_number='5',
                                         vegan=False)
        recipe_3 = Recipe.objects.create(name='pizza mix',
                                         description='This is a mix pizaa',
                                         like_number='0',
                                         vegan=False)

        beef = Ingredient.objects.create(name='beef', vegan=False)
        chicken = Ingredient.objects.create(name='chicken', vegan=False)
        mushroom = Ingredient.objects.create(name='mushroom', vegan=True)
        salad = Ingredient.objects.create(name='salad', vegan=True)
        recipe_1.ingredients.add(mushroom,salad)
        recipe_2.ingredients.add(chicken, beef)
        recipe_3.ingredients.add(mushroom, beef, chicken)

    def test_api_response_is_correct(self):
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()['data']) == 3)

    def test_api_response_order_is_by_popularity(self):
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.json()['data'][0]['like_number'], 20)
        self.assertEqual(response.json()['data'][1]['like_number'], 5)
        self.assertEqual(response.json()['data'][2]['like_number'], 0)

    def test_if_a_recipe_is_vegan(self):
        response = self.client.get('/api/recipes/')
        veg_pizza = response.json()['data'][0]
        ingredients = veg_pizza['recipe_ingredients']
        is_expected_recipe_vegan = all([ingredient['vegan'] for ingredient in ingredients])
        self.assertEqual(is_expected_recipe_vegan, veg_pizza['vegan'])

    def test_if_a_recipe_is_not_vegan(self):
        response = self.client.get('/api/recipes/')
        mix_pizza = response.json()['data'][2]
        ingredients = mix_pizza['recipe_ingredients']
        is_expected_recipe_vegan = all([ingredient['vegan'] for ingredient in ingredients])
        self.assertEqual(is_expected_recipe_vegan, mix_pizza['vegan'])

class RecipePostApiTests(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='beef', vegan=False)
        Ingredient.objects.create(name='salad', vegan=True)

    def test_post_recipe_api(self):
        expected_data = {
            'ingredients': ['beef', 'salad'],
            'params':{
                'name': 'new_pizza',
                'description' : 'This is a new one',
                'like_number' : 1}
        }
        post_response = self.client.post('/api/recipes/', expected_data ,content_type='application/json')
        self.assertEqual(post_response.status_code, 200)
        get_response = self.client.get('/api/recipes/')
        actual_data = get_response.json()['data']
        self.assertTrue(len(actual_data) == 1)
        self.assertEqual(actual_data[0]['name'], expected_data['params']['name'])
        actual_ingredients = [ingredient['name'] for ingredient in actual_data[0]['recipe_ingredients']]
        self.assertEqual(sorted(actual_ingredients), sorted(expected_data['ingredients']))

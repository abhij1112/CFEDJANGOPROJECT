from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Recipe,RecipeIngredients

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe',password='abc123')

    def test_user_pw(self):
        checked = self.user_a.check_password('abc123')
        self.assertTrue(checked)
        
class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe',password='abc123')
        self.recipe_a = Recipe.objects.create(
            name = 'grileed chicken',
            user = self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name = 'grilled chicken tacos',
            user = self.user_a
        )
        
        self.recipe_ingredient_a = RecipeIngredients.objects.create(
            recipe = self.recipe_a,
            name = 'chicken',
            quantity = '1/2',
            unit = 'kg'
        )
        
        self.recipe_ingredient_b = RecipeIngredients.objects.create(
            recipe = self.recipe_a,
            name = 'chicken',
            quantity = 'abdf',
            unit = 'kg'
        )
        
    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(),1)
        
    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(),2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(),2)
        
    def test_recipe_igredients_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredients_set.all()
        self.assertEqual(qs.count(),2)
        
    def test_recipe_ingredientscount(self):
        recipe = self.recipe_a
        qs = RecipeIngredients.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(),2)
        
    def test_user_two_level_relation(self):
        user =self.user_a
        qs = RecipeIngredients.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(),2)
        
    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        recipeingredients_ids = list(user.recipe_set.all().values_list('recipeingredients__id',flat=True))
        qs = RecipeIngredients.objects.filter(id__in = recipeingredients_ids)
        self.assertEqual(qs.count(),2)
        
    def test_user_two_level_relation(self):
        user =self.user_a
        ids = user.recipe_set.all().values_list('id',flat=True)
        qs = RecipeIngredients.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(),2)
        
    def test_unit_measure_validation(self):
        invalid_unit = 'ounce'
        
        ingredient = RecipeIngredients(
            name = 'New',
            quantity = 10,
            recipe=self.recipe_a,
            unit= invalid_unit
        )
        ingredient.full_clean()
        
    def test_unit_measure_validation_error(self):
        invalid_units = ['nada','ajdnj']
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredients(
                        name = 'New',
                        quantity = 10,
                        recipe=self.recipe_a,
                        unit= unit
                )
                ingredient.full_clean()
    
    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)   
           

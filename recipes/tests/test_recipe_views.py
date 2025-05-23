from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views

class RecipeViewsTest(TestCase):
    
    # ========= Tests from home ==========
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    
    def test_recipe_home_view_resturn_status_code_200_OK(self):
        resolve = self.client.get(reverse('recipes:home'))
        self.assertEqual(resolve.status_code, 200)  
        
    def test_recipe_home_view_loads_correct_template(self):
        resolve = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(resolve, 'recipes/pages/home.html')
    
    def test_recipe_home_template_shows_no_recipes_found_message(self):
        resolve = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found here!', resolve.content.decode('utf-8'))
        
    # ========= Tests from category ==========
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_view_resturn_404_if_no_recipes_found(self):
        resolve = self.client.get(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertEqual(resolve.status_code, 404)  
    
    # ========= Tests from recipe/detail ==========
        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        
    def test_recipe_detail_view_resturn_404_if_no_recipes_found(self):
        resolve = self.client.get(reverse('recipes:recipe', kwargs={'id': 2}))
        self.assertEqual(resolve.status_code, 404)
    
        
        

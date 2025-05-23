from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeViewsTest(RecipeTestBase):
    
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
        
    def test_recipe_home_template_loads_recipes(self): #criando dados ficticios para teste
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)
    
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
    
        
        

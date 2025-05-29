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
        self.make_recipe()
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        
        #Check if one recipe exists
        self.assertIn(
            '<h1>No recipes found here!</h1>',
            response.content.decode('utf-8')
        ) 
    
    # ========= Tests from category ==========
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_view_resturn_404_if_no_recipes_found(self):
        resolve = self.client.get(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertEqual(resolve.status_code, 404)  
        
    def test_recipe_category_template_loads_recipes(self): #criando dados ficticios para teste
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
        
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse(
                'recipes:category', 
                kwargs={'category_id':recipe.category.id}
                )
            )
        
        #Check if one recipe exists
        self.assertEqual(response.status_code, 404)
    
    # ========= Tests from recipe/detail ==========
        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        
    def test_recipe_detail_view_resturn_404_if_no_recipes_found(self):
        resolve = self.client.get(reverse('recipes:recipe', kwargs={'id': 2}))
        self.assertEqual(resolve.status_code, 404)
        
    def test_recipe_detail_template_loads_the_correct_recipe(self): #criando dados ficticios para teste
        needed_title = 'This is a detail page - It load one recipe'
        
        self.make_recipe(title=needed_title)
        
        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'id':1}
                )
            )
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
        
    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'id':recipe.id}
                )
            )
        
        #Check if one recipe exists
        self.assertEqual(response.status_code, 404)
        
    
    # search
    def test_recipes_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot',
            response.content.decode('utf-8')
        )
        
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
        
        

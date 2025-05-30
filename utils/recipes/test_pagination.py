from unittest import TestCase
from utils.recipes.pagination import make_pagination_range
from django.urls import resolve, reverse
from recipes.tests.test_recipe_base import RecipeTestBase


class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # Current page = 1 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        # Current page = 4 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)
        
    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 14 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Current page = 18 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 19 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 20 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 21 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        
    def test_recipes_viwes_for_page(self):
        # Criar 10 receitas
        for i in range(1, 11):
            self.make_recipe(
                slug=str(i),
                title=f'This is recipe {i}',
                author_data={'username': str(i)}
            )

        current_page = 1
        url = reverse('recipes:home')
        response = self.client.get(f'{url}?page={current_page}')

        expected_items_per_page = 9

        # CORREÇÃO AQUI:
        self.assertEqual(expected_items_per_page, len(response.context['recipes'].object_list))
       
        
        
        
        
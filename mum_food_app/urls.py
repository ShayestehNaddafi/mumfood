from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^recipes/$', views.RecipeListByPopularityView.as_view(),
            name='RecipeListByPopularityView'),
    re_path(r'^ingredient/$', views.IngredientView.as_view(),
            name='IngredientView'),
    re_path(r'^recipe/(?P<recipe_id>\w+)/$', views.RecipeView.as_view(),
            name='RecipeView'),
]
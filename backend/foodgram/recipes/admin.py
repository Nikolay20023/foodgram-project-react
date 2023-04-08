from django.contrib import admin
from .models import (
    Tag,
    Recipe,
    RecipeIngredient,
    Favourite,
    ShoppingCart,
    Ingredient
)

# Register your models here.
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Favourite)
admin.site.register(ShoppingCart)
admin.site.register(Ingredient)

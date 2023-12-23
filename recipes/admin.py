from django.contrib.auth import get_user_model
from django.contrib import admin

# Register your models here.
from .models import RecipeIngredients , Recipe , RecipeIngredientsImage

User = get_user_model()

admin.site.register(RecipeIngredients)

admin.site.register(RecipeIngredientsImage)


class RecipeIngredientsInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0
    #fields = ['name','quantity','unit','directions']
    readonly_fields = ['quantity_as_float','as_mks','as_imperial']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline]
    list_display = ['name','user']
    readonly_fields = ['timestamp','updated']
    raw_id_fields = ['user']

admin.site.register(Recipe,RecipeAdmin)



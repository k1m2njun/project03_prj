from django.contrib import admin
from .models import Ingredients, MnistImage, Categories, Tags, Comment, RecipePost

admin.site.register(Ingredients)

admin.site.register(MnistImage)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}
    
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}

admin.site.register(Categories, CategoryAdmin)

admin.site.register(Tags, TagAdmin)

admin.site.register(Comment)

admin.site.register(RecipePost)
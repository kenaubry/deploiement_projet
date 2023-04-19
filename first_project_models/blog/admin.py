from django.contrib import admin

from .models import Post, Author, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'excerpt', 'content', 'author__first_name', 'author__last_name']
    list_filter = ['date', 'author']
    list_display = ['title', 'author_name', 'date', 'display_tags']
    list_display_links = ['author_name']
    list_editable = ['title']
    fieldsets = [
        ('Content', {'fields': ['title', 'excerpt', 'content', 'image_name', 'tags']}),
        ('Metadata', {'fields': ['author', 'slug']}),
    ]
    actions = ['change_author']

    def change_author(self, request, queryset):
        # URL de la nouvelle vue qui affichera le formulaire de sélection d'auteur
        url = reverse('admin:select_author')
        # Bouton pour ouvrir la nouvelle fenêtre
        button = f'<a href="{url}" target="_blank">Select a new author</a>'
        return format_html(button)

    change_author.short_description = "Change author of selected posts"

    def author_name(self, obj):
        return obj.author.first_name + ' ' + obj.author.last_name

    author_name.short_description = 'Author'

    def display_tags(self, obj):
        return ', '.join(tag.caption for tag in obj.tags.all())

    display_tags.short_description = 'Tags'

admin.site.register(Post, PostAdmin)

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)


# Register your models here.

'''
L'erreur admin.E109 signifie que le champ spécifié dans list_display à l'index 3 
(tags dans votre cas) est un champ ManyToManyField, ce qui n'est pas autorisé. 
list_display ne peut inclure que des champs de modèle simples, tels que CharField ou IntegerField, 
et non des relations telles que des clés étrangères ou des champs ManyToMany.

L'erreur admin.E124 signifie que list_editable ne peut être utilisé que si list_display_links
 est également défini. list_display_links est utilisé pour spécifier les champs qui doivent être 
 liés à la page de détails de l'objet, et ne peut inclure que des champs simples de modèle. 
 Dans votre cas, vous pouvez utiliser list_display_links = ['title'] car title est un champ simple de modèle.'''

# FORMULAIRE CHOIX ADMIN

from django.urls import reverse
from django.utils.html import format_html



# Nouvelle vue pour afficher le formulaire de sélection d'auteur

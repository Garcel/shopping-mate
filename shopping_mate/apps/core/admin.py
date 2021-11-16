from django.contrib import admin

from shopping_mate.apps.core import models as m


class ShoppingItemInline(admin.TabularInline):
    model = m.ShoppingItem
    extra = 0


@admin.register(m.ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'description', 'creation_date', 'last_update')
    ordering = ('owner', 'creation_date', 'last_update')
    search_fields = ('name', 'owner')

    inlines = [ShoppingItemInline, ]


@admin.register(m.ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = ('list', 'name', 'description', 'creation_date', 'last_update', 'due_date')
    ordering = ('list', 'creation_date', 'last_update', 'due_date')
    search_fields = ('name', 'list')

from django.urls import path
from .models import *
from myapp.helpers.parse_menu_data_helper import ParseDataMenu
from django.contrib import admin
from django.http import HttpResponseRedirect



class DishInline(admin.TabularInline):
    model = Dish
    extra = 2


class CategoryAdmin(admin.ModelAdmin, ParseDataMenu):
    inlines = [DishInline, ]
    change_list_template = "admin/model_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_menu/', self.update_menu),
        ]
        return my_urls + urls

    def update_menu(self, request):
        self.parse_data()
        self.message_user(request, "Menu is updated")
        return HttpResponseRedirect("/admin/myapp/category/")





admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.site_header = "Garage Admin"



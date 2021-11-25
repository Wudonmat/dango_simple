from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import MyUser, Dog


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "username", "address", "is_admin",)
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {
            "fields":("username", "email", "password")
        }),
        ("User Info", {"fields": ("address",)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (None, {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", ),
            },),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


class DogAdmin(admin.ModelAdmin):
    list_display = (
         "dog_breed", "size",
        )
    search_fields = ("dog_breed", "size",)


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.unregister(Group)
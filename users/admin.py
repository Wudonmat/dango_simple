from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import MyUser, MyUserInfo, Dog, Area


class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ("email", "username", "is_admin",)
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Info", {"fields": ("email", "username", "password",)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


class MyUserInfoAdmin(admin.ModelAdmin):
    list_display = (
         "birth_date", "gender",
        )
    search_fields = ("gender",)


class DogAdmin(admin.ModelAdmin):
    list_display = (
         "dog_breed", "size",
        )
    search_fields = ("dog_breed", "size",)


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(MyUserInfo, MyUserInfoAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.unregister(Group)
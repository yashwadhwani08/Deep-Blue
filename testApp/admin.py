from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import TestUserCreationForm, TestUserChangeForm
from .models import Task, User

# Register your models here.


class TestAppUserAdmin(UserAdmin):
    add_form = TestUserCreationForm
    form = TestUserChangeForm
    model = User
    ordering = ('email',)
    list_display = ('email', 'phone', 'date_joined',
                    'last_login', 'is_admin', 'is_staff',)
    search_fields = ('email', 'phone',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_admin', 'is_superuser', 'is_verified',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    # search_fields = ('email',)

    # exclude = ('username',)
    # fieldsets = ((None, {
    #     'fields': ('email', 'password','phone', 'date_joined',
    #                'last_login', 'is_admin', 'is_staff', 'is_superuser')
    # }),)

    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )


# add_fieldsets = (
#     (None, {
#         'classes': ('wide',),
#         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#      ),
# )


admin.site.register(User, TestAppUserAdmin)
admin.site.register(Task)

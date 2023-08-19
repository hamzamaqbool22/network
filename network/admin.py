from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile,Newpost,Like

# Register the custom User model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Newpost)
admin.site.register(Like)
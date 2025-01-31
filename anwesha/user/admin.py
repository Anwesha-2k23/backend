from django.contrib import admin
from .models import User,AppUsers
from utility import export_as_csv
from .utility import mail_content, send_email_using_microservice

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Custom admin class for User model.
    """

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        """
        Admin action to lock selected users.
        """
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    @admin.action(description='Resend Verification Mail')
    def resend_mail(self, request, queryset):
        """
        Admin action to resend verification mail to selected users.
        """
        for obj in queryset:
            anwesha_id = obj.anwesha_id
            email = obj.email_id
            fullname = obj.full_name
            body = mail_content(type=1, email_id=email, anwesha_id=anwesha_id, full_name=fullname)
            send_email_using_microservice(
                email_id=email,
                subject="No reply",
                text=body
            )
        self.message_user(request, "Email sent again")

    list_display = ('anwesha_id', 'full_name', 'email_id', 'collage_name')
    actions = [lock_user, export_as_csv, resend_mail]
    list_filter = ('user_type', 'is_locked', 'collage_name')
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'anwesha_id',
                'full_name',
                'email_id',
                'phone_number',
                'profile_photo',
                ('age', 'gender'),
                'user_type'
            )
        }),
        ('Social Links', {
            'fields': ('instagram_id', 'facebook_id', 'collage_name', 'qr_code')
        }),
        ('Internal Flags', {
            'fields': (
                ('accomadation_selected', 'is_profile_completed'),
                ('is_email_verified', 'is_locked', 'is_loggedin'),
                'password',
                ('secret', 'signature')
            )
        })
    )
    empty_value_display = '-empty-'
    search_fields = ['full_name', 'anwesha_id', 'email_id', 'phone_number', 'collage_name']

@admin.register(AppUsers)
class AppUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email_id', 'is_logged_in')  
    search_fields = ('id', 'phone_number', 'email_id')  
    list_filter = ('is_logged_in',)  
    ordering = ('id',)
    readonly_fields = ('id',) 

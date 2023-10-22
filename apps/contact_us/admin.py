from django.contrib import admin

from .models import ContactForm, ContactUs, EmployeeContact, Phone, SocialMedia


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("address", "email")
    search_fields = ("address", "email")


@admin.register(EmployeeContact)
class EmployeeContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    search_fields = ("name", "phone", "email")


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("phone",)
    search_fields = ("phone",)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    search_fields = ("name", "url")


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")

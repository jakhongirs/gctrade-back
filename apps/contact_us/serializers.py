from rest_framework import serializers

from .models import (
    AboutUs, ContactForm, ContactUs, EmployeeContact, Phone, SocialMedia
)


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ("phone",)


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = (
            "name",
            "url",
        )


class EmployeeContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeContact
        fields = (
            "name",
            "image",
            "phone",
            "email",
            "telegram_username",
        )


class ContactUsSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(many=True)
    social_media = SocialMediaSerializer(many=True)

    class Meta:
        model = ContactUs
        fields = ("phone", "email", "longitude", "latitude", "address", "social_media")


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ("name", "email", "phone", "question")


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ("cover", "title", "description")

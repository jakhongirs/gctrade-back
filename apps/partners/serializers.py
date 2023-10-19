from rest_framework import serializers

from .models import Company, Feedback, Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ("id", "name", "logo", "url", "order")


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "logo", "url")


class FeedbackSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ("id", "company", "text")

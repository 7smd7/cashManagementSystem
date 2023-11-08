from .models import Transaction
from rest_framework import serializers
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
import requests


class UserSerializer(serializers.ModelSerializer):
    """
    Serailizer to validate and create a new user
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


def is_amount(value):
    if value <= 0:
        raise serializers.ValidationError({"detail": "Invalid Amount"})
    return value


class CreateTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(validators=[is_amount], max_digits=100, decimal_places=2)

    def save(self):
        user = self.context['request'].user
        data = self.context['request'].data
        transaction = Transaction.objects.create(
            user=user,
            transaction_type=data["transaction_type"],
            category_type=data["category_type"],
            amount=data["amount"],
        )

        return TransactionSerializer(transaction).data


class ReportSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES, required=False)
    category_type = serializers.ChoiceField(choices=Transaction.CATEGORY_TYPES, required=False)
    year = serializers.DateTimeField(required=False)
    quarter = serializers.DateTimeField(required=False)
    month = serializers.DateTimeField(required=False)
    week = serializers.DateTimeField(required=False)
    day = serializers.DateTimeField(required=False)
    hour = serializers.DateTimeField(required=False)
    minute = serializers.DateTimeField(required=False)
    second = serializers.DateTimeField(required=False)
    sum = serializers.DecimalField(decimal_places=2, max_digits=100)
    count = serializers.IntegerField()

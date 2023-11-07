from django.contrib import admin

from app.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transaction_type', 'category_type', 'amount', 'timestamp']
    filter = (
        'transaction_type',
        'category_type',
        'timestamp',
        'user__username',
    )

from django.urls import path
from .views import Login, Register, UserInfo, TransactionViewSet

transaction_list = TransactionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

transaction_detail = TransactionViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('user_info/', UserInfo.as_view()),
    path('transactions/', transaction_list),
    path('transactions/<int:pk>/', transaction_detail),
]
from django.db.models import Sum, Count
from django.db.models.functions import Trunc

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Transaction
from .serializers import UserSerializer, TransactionSerializer, CreateTransactionSerializer, ReportSerializer


class Login(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key, "username": username})
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class Register(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserInfo(APIView):

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        data = UserSerializer(user).data
        deposit = Transaction.objects.filter(
            user=user,
            transaction_type="deposit").aggregate(Sum('amount'))['amount__sum']
        withdrawal = Transaction.objects.filter(
            user=user,
            transaction_type="withdrawal").aggregate(Sum('amount'))['amount__sum']
        data['balance'] = (deposit if deposit else 0) - (withdrawal if withdrawal else 0)
        return Response(data)


class TransactionViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = (
        'transaction_type',
        'category_type',
        'category_type',
    )
    ordering_fields = ('transaction_type', 'category_type', 'category_type', 'amount', 'timestamp')

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateTransactionSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        resp = serializer.save()
        return Response(resp)


class Reports(APIView):
    def get(self, request, *args, **kwargs):
        group_by = request.GET['group_by'].split(';')
        transactions = Transaction.objects.filter(user=request.user)
        trunc_list = ["year", "quarter", "month", "week", "day", "hour", "minute", "second"]
        trunc_dict = {i: Trunc('timestamp', kind=i) for i in trunc_list}
        transactions = transactions.annotate(**trunc_dict)
        reports = transactions.values(*group_by).annotate(
            sum=Sum('amount'), count=Count('id')
        ).values(*group_by, 'count', 'sum').order_by(*group_by)
        return Response(ReportSerializer(reports, many=True).data)

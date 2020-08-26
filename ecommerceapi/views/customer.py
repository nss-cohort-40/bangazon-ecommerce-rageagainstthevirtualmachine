"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer, PaymentType
from .user import UserSerializer


class PaymenttypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for payment types
        Args:
            serializer.HyperlinkedModelSerializer
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype', lookup_field='id')
        fields = ('id', 'url', 'merchant_name', 'account_number',
                  'expiration_date', 'created_at', 'customer_id')


class CustomerWithPaymentsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for customers
        Args:
            serializer.HyperlinkedModelSerializer
    """
    user = UserSerializer()
    paymenttypes = PaymenttypeSerializer(many=True)

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer', lookup_field='id')
        fields = ('id', 'url', 'address', 'phone_number',
                  'user_id', 'user', 'paymenttypes')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for customers
        Args:
            serializer.HyperlinkedModelSerializer
    """
    user = UserSerializer()
    paymenttypes = PaymenttypeSerializer(many=True)

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer', lookup_field='id')
        fields = ('id', 'url', 'address', 'phone_number',
                  'user_id', 'user')


class Customers(ViewSet):
    """Customers for ecommerce API"""

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single customer instance
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            customer.paymenttypes = PaymentType.objects.filter(
                customer_id=customer.id)
            serializer = CustomerWithPaymentsSerializer(
                customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to customer resource
        Returns:
            Response -- JSON serialized list of customers
        """
        customers = Customer.objects.all()
        serializer = CustomerSerializer(
            customers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

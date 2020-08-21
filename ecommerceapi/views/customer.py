"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer
from .user import UserSerializer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for customers
        Args:
            serializer.HyperlinkedModelSerializer
    """
    user = UserSerializer()

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer', lookup_field='id')
        fields = ('id', 'url', 'address', 'phone_number', 'user_id', 'user')


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
            serializer = CustomerSerializer(
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

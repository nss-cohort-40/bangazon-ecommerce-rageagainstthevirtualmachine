"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Order, PaymentType, Customer
from .customer import CustomerSerializer
from .paymenttype import PaymentTypeSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for orders
        Args:
            serializer.HyperlinkedModelSerializer
    """
    # ! Uncomment below to provide nested related data
    # customer = CustomerSerializer()
    # paymenttype = PaymentTypeSerializer()

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order', lookup_field='id')
        fields = ('id', 'url', 'created_at', 'customer_id',
                  'customer', 'paymenttype_id', 'paymenttype')


class Orders(ViewSet):
    """Orders for ecommerce API"""

    def create(self, request):
        """
        Handle POST operations
        Returns:
            Response -- JSON serialized Order instance
        """

        neworder = Order()
        neworder.customer_id = request.data["customer_id"]
        neworder.paymenttype_id = request.data["paymenttype_id"]
        neworder.save()

        serializer = OrderSerializer(
            neworder, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single order instance
        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(
                order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to order resource
        Returns:
            Response -- JSON serialized list of orders
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import OrderProduct

# ! Uncomment below to provide nested related data
# from ecommerceapi.models import Product, Order
# from .product import ProductSerializer
# from .order import OrderSerializer


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for orderproducts
        Args:
            serializer.HyperlinkedModelSerializer
    """
    # ! Uncomment below to provide nested related data
    # product = ProductSerializer()
    # paymenttype = PaymentTypeSerializer()

    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='order', lookup_field='id')
        fields = ('id', 'url', 'order_id', 'product_id')


class OrderProducts(ViewSet):
    """OrderProducts for ecommerce API"""

    def create(self, request):
        """
        Handle POST operations
        Returns:
            Response -- JSON serialized OrderProducts instance
        """

        neworderproduct = OrderProduct()
        neworderproduct.customer_id = request.data["customer_id"]
        neworderproduct.paymenttype_id = request.data["paymenttype_id"]
        neworderproduct.save()

        serializer = OrderProductSerializer(
            neworderproduct, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single orderproduct instance
        Returns:
            Response -- JSON serialized orderproduct instance
        """
        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                orderproduct, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to orderproduct resource
        Returns:
            Response -- JSON serialized list of orderproducts
        """
        orderproducts = OrderProduct.objects.all()
        serializer = OrderProductSerializer(
            orderproducts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

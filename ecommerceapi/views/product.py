"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product
from .customer import CustomerSerializer


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for products
        Args:
            serializer.HyperlinkedModelSerializer
    """

    # ! Uncomment below to provide nested related data
    customer = CustomerSerializer()

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product', lookup_field='id')
        fields = ('id', 'url', 'name', 'description',
                  'customer_id', 'customer', 'producttype_id', 'producttype')
        depth = 1


class Products(ViewSet):
    """Products for ecommerce API"""

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single product instance
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to product resource
        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

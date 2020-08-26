"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import ProductType
from .product import ProductSerializer


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for product types
        Args:
            serializer.HyperlinkedModelSerializer
    """
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype', lookup_field='id')
        fields = ('id', 'url', 'name', 'products')
        depth = 1


class ProductTypes(ViewSet):
    """ProductTypes for ecommerce API"""

    def create(self, request):
        """
        Handle POST operations
        Returns:
            Response -- JSON serialized ProductType instance
        """

        newproducttype = ProductType()
        newproducttype.name = request.data["name"]
        newproducttype.save()

        serializer = ProductTypeSerializer(
            newproducttype, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single producttype instance
        Returns:
            Response -- JSON serialized producttype instance
        """
        try:
            producttype = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(
                producttype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to producttype resource
        Returns:
            Response -- JSON serialized list of producttypes
        """
        producttypes = ProductType.objects.all()
        serializer = ProductTypeSerializer(
            producttypes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

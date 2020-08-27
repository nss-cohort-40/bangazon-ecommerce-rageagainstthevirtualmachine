"""View module for handling requests about customers"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import PaymentType, Customer
from .customer import CustomerSerializer


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for payment types
        Args:
            serializer.HyperlinkedModelSerializer
    """
    # customer = CustomerSerializer()

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype', lookup_field='id')
        fields = ('id', 'url', 'merchant_name', 'account_number',
                  'expiration_date', 'created_at', 'customer_id', 'customer')


class PaymentTypes(ViewSet):
    """PaymentTypes for ecommerce API"""

    def create(self, request):
        """
        Handle POST operations
        Returns:
            Response -- JSON serialized PaymentType instance
        """

        newpaymenttype = PaymentType()
        newpaymenttype.merchant_name = request.data["merchant_name"]
        newpaymenttype.account_number = request.data["account_number"]
        newpaymenttype.expiration_date = request.data["expiration_date"]
        # newpaymenttype.customer_id = request.data["customer_id"]
        newpaymenttype.customer = Customer.objects.get(user=request.auth.user)
        newpaymenttype.save()

        serializer = PaymentTypeSerializer(
            newpaymenttype, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single paymenttype instance
        Returns:
            Response -- JSON serialized paymenttype instance
        """
        try:
            paymenttype = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(
                paymenttype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to paymenttype resource
        Returns:
            Response -- JSON serialized list of paymenttypes
        """
        paymenttypes = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(
            paymenttypes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

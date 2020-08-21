"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for users
        Args:
            serializer.HyperlinkedModelSerializer
    """

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user', lookup_field='id')
        fields = ('id', 'first_name', 'last_name',
                  'email', 'last_login', 'date_joined')


class UserViewSet(ViewSet):
    """User Viewset"""
    serializer_class = UserSerializer
    user = User.objects.all()

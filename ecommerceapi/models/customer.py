"""
    Customer Model
    exports class:Customer
    generated by: Bryan Nilsen
"""
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    Stores the properties of a single customer
    Inherits: created_at from CreatedAt class
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user")
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=55)


    class Meta:
        verbose_name = ("customer")
        verbose_name_plural = ("customers")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

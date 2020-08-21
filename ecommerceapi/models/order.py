"""
    Order Model
    exports class: Order
    generated by: Bryan Nilsen
"""
from django.db import models
from .createdat import CreatedAt
from .customer import Customer
from .paymenttype import PaymentType


class Order(CreatedAt):
    """
    Stores the properties of a single order.
    Inherits: created_at from CreatedAt class
    Related Data: Customer
    """

    # Related Data
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="orders")
    paymenttype = models.ForeignKey(
        PaymentType, on_delete=models.DO_NOTHING, related_name="orders"
    )

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")

    def __str__(self):
        return f'Order No. {self.id}'
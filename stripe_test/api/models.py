from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.sessions.models import Session


class Discount(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200,
        blank=True,
        null=True
    )
    discount = models.PositiveIntegerField(
        'Проценты',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    discount_id = models.SlugField(
        'id',
        unique=True,
        blank=True,
        null=True,
        max_length=200
    )

    def __str__(self):
        return f'{self.name}'


class Tax(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200,
        blank=True,
        null=True
    )
    tax = models.PositiveIntegerField(
        'Проценты',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    tax_id = models.SlugField(
        'id',
        unique=True,
        blank=True,
        null=True,
        max_length=200
    )

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200
    )
    description = models.CharField(
        'Описание',
        max_length=200
    )
    price = models.PositiveIntegerField(
        'Цена'
    )

    tax = models.ManyToManyField(
        Tax,
        verbose_name='Налог',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-price']

    def __str__(self):
        return f'{self.name}'

    def get_display_price(self):
        return f'{self.price/100}'


class BasketItem(models.Model):
    item = models.ForeignKey(
        Item,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        verbose_name='Order'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )

    def get_display_price(self):
        return f'{self.item.price/100*self.quantity}'


class Order(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        unique=True,
        blank=True,
        null=True
    )
    basket_item = models.ManyToManyField(
        Item,
        verbose_name='Товар',
        through='BasketItem',
        null=True,
        blank=True
    )
    discount = models.ForeignKey(
        Discount,
        verbose_name='Скидка',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.session}'

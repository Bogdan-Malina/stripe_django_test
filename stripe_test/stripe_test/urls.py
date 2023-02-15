from django.contrib import admin
from django.urls import path

from api.views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    StripeIntentView,
    IndexPageView,
    ItemPageView,
    AddBasketView,
    OrderPageView,
    CreateCheckoutSessionForOrderView
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'create-payment-intent/<pk>',
        StripeIntentView.as_view(),
        name='create-payment-intent'
    ),
    path(
        'cancel/',
        CancelView.as_view(),
        name='cancel'
    ),
    path(
        'success/',
        SuccessView.as_view(),
        name='success'
    ),
    path(
        '',
        IndexPageView.as_view(),
        name='index'
    ),
    path(
        'order/',
        OrderPageView.as_view(),
        name='order'
    ),
    path(
        'item/<pk>',
        ItemPageView.as_view(),
        name='item'
    ),
    path(
        'add/<pk>/',
        AddBasketView.as_view(),
        name='add'
    ),
    path(
        'buy/<pk>/',
        CreateCheckoutSessionView.as_view(),
        name='buy'
    ),
    path(
        'buy-order/',
        CreateCheckoutSessionForOrderView.as_view(),
        name='buy-order'
    ),
]

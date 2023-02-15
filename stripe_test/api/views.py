import json

from .models import Item, Order, BasketItem
from django.contrib.sessions.models import Session

from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class IndexPageView(TemplateView):
    template_name = 'index.html'
    session_key = None

    def get(self, request, *args, **kwargs):
        self.session_key = request.session.session_key
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        items = Item.objects.all()
        order = Order.objects.filter(session=self.session_key)
        basket = None
        if order:
            basket = BasketItem.objects.filter(order=order[0])
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context.update({
            'basket': basket,
            'items': items,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


def get_taxes(tax_basket_item):
    taxes = []
    for tax in tax_basket_item:
        if not tax.tax_id:
            new_tax = stripe.TaxRate.create(
                display_name=tax.name,
                inclusive=False,
                percentage=tax.tax,
                country="US",
                state="CA",
                jurisdiction="US - CA",
            )
            tax.tax_id = new_tax['id']
            tax.save()
        taxes.append(tax.tax_id)
    return taxes


class CreateCheckoutSessionForOrderView(View):
    def get(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://51.250.84.205:8000/'
        session_key = request.session.session_key
        order = Order.objects.filter(session=session_key)
        basket_items_all = BasketItem.objects.filter(order=order[0])
        discounts_basket_item = order[0].discount
        coupon = []

        if discounts_basket_item:
            if not discounts_basket_item.discount_id:
                new_discount = stripe.Coupon.create(
                    percent_off=discounts_basket_item.discount,
                    duration="repeating",
                    duration_in_months=12
                )
                discounts_basket_item.discount_id = new_discount['id']
                discounts_basket_item.save()
            coupon.append(
                {'coupon': discounts_basket_item.discount_id}
            )

        items = []
        metadata = []

        for basket_item in basket_items_all:
            tax_basket_item = basket_item.item.tax.all()

            taxes = get_taxes(tax_basket_item)

            items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': basket_item.item.name,
                    },
                    'unit_amount': basket_item.item.price,
                },
                'quantity': basket_item.quantity,
                'tax_rates': taxes
            })
            metadata.append([
                f'{basket_item.item.id}',
            ])

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            metadata=metadata,
            mode='payment',
            discounts=coupon,
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({
            'id': session.id,
        })


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = Item.objects.get(id=product_id)
        YOUR_DOMAIN = 'http://51.250.84.205:8000/'
        taxes = get_taxes(product.tax.all())

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': product.price,
                },
                'quantity': 1,
                'tax_rates': taxes
            }],
            metadata={
                'product_id': product.id,
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': session.id,
        })


class AddBasketView(View):
    def post(self, request, *args, **kwargs):
        if not request.session or not request.session.session_key:
            request.session.save()

        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        item = Item.objects.get(id=kwargs.get('pk'))

        order = Order.objects.filter(
            session=session,
        )

        if not order:
            new_order = Order.objects.create(
                session=session,
            )
            BasketItem.objects.create(
                order=new_order,
                item=item,
                quantity=1
            )
        else:
            basket_item = BasketItem.objects.filter(
                order=order[0],
                item=item
            )

            if basket_item:
                basket_item = BasketItem.objects.get(
                    order=order[0],
                    item=item
                )
                basket_item.quantity += 1
                basket_item.save()
            else:
                BasketItem.objects.create(
                    order=order[0],
                    item=item,
                    quantity=1
                )

        return JsonResponse({
            'clientSecret': kwargs
        })


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Item.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })


class ItemPageView(TemplateView):
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        item_id = kwargs.get('pk')
        item = Item.objects.get(id=item_id)
        context = super(ItemPageView, self).get_context_data(**kwargs)
        context.update({
            'item': item,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class OrderPageView(TemplateView):
    template_name = 'order.html'
    session_key = None

    def get(self, request, *args, **kwargs):
        self.session_key = request.session.session_key
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context_order = None
        order = Order.objects.filter(session=self.session_key)
        basket = None
        if order:
            context_order = order[0]
            basket = BasketItem.objects.filter(order=order[0])

        context = super(OrderPageView, self).get_context_data(**kwargs)
        context.update({
            'order': context_order,
            'basket': basket,
            'product': basket,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context

from .models import Payment
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_price(product_id, amount):
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        currency='usd',
        product=product_id,
    )
    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return session


def save_payment(user, course, lesson, amount, session_id):
    payment = Payment.objects.create(
        user=user,
        paid_course=course,
        paid_lesson=lesson,
        amount=amount,
        payment_method='stripe',
        stripe_session_id=session_id,
    )
    return payment

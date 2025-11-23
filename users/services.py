from typing import Tuple

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str) -> str:
    """Создание продукта в Stripe"""
    try:
        product = stripe.Product.create(
            name=name,
        )
        return product.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании продукта: {str(e)}")


def create_stripe_price(product_id: str, amount: float, currency: str = "rub") -> str:
    """Создание цены. amount — в рублях"""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount) * 100,  # Stripe принимает целое число в минимальных единицах
            currency=currency,
        )
        return price.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании цены: {str(e)}")


def create_stripe_session(price_id: str, success_url: str, cancel_url: str) -> Tuple[str, str]:
    """Создание платёжной сессии"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.id, session.url
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании сессии: {str(e)}")


def get_stripe_session_status(session_id):
    """Получение статуса платежа"""
    session = stripe.checkout.Session.retrieve(session_id)
    return {"status": session.payment_status}

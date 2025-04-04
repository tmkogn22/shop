import time
from datetime import date
from catalog.models import Order, Discount
from users.models import CustomUser
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def example_task():
    time.sleep(3)
    return 'EXAMPLE~TASK'


@shared_task
def example_schedule_task():
    time.sleep(3)
    return 'SCHEDULE TASK'


@shared_task
def check_paid_orders():
    orders = Order.objects.filter(payment_status='Paid')

    for order in orders:
        send_mail(
            subject='Order on EXAMPLE SHOP',
            message=f'Your order {order.id} is paid and will be boxed soon!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user.email, ]
        )


@shared_task
def broadcast_discount_info():
    discounts = Discount.objects.all()
    current_date = date.today()
    valid_disc = []
    for discount in discounts:
        delta = (current_date - discount.exp_date)
        if delta.days <= 0:
            valid_disc.append(discount)

    users = CustomUser.objects.filter(is_sub=True)
    send_mail(
        subject='Discounts on EXAMPLE SHOP',
        message=', '.join(f'{discount.name} - {discount.percent} UNTIL {discount.exp_date}' for discount in valid_disc),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=users
    )


@shared_task
def send_order_notification():
    orders = Order.objects.all()
    for order in orders:
        if not order.is_notif_sent:
            if order.notification_time == 1:
                time_notif = 'in an hour'
            elif order.notification_time == 6:
                time_notif = 'in 6 hours'
            else:
                time_notif = 'in 24 hours'

            send_mail(
                subject='DELIVERY NOTIFICATION',
                message=f'Your order {order.id} will be delivered in {time_notif}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.user.email]
            )
            order.is_notif_sent = True
            order.save()


from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import Order
from .models import OrderConfirmation
from django.contrib import messages
import redis
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
import pickle
import dill
from django.db import connection
from .forms import OrderCreateForm
from django import forms

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@task(name="process_order")
def process_order(first_name, last_name, email, address,
                                            postal_code, city):

    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address,
                                            postal_code=postal_code, city=city)

    #print("Read order from DB")
    # order = Order.objects.get(id=order_id)
    #
    cart = dill.loads(r.get('cart'))
   
    for item in cart :
	try:
                #Order is created in database here
		OrderItem.objects.create(order=order,
	                                     product=item['product'],
	                                     price=item['price'],
	                                     quantity=item['quantity'])
        except:
		pass
	        cart.clear()
	        
	#Order is read from database

	#Select full_name,last_name,address from orders_order where id=' + order.id	
	#order = Order.objects.raw('Select full_name,last_name,address from orders_order where id=' + order.id)
	#order = Order.objects.raw('Select id,first_name,last_name,address from orders_order where id=1')
	sql = 'Select orders_order.id, orders_order.first_name, orders_order.last_name, orders_order.address, orders_orderitem.product_id, orders_orderitem.price, orders_orderitem.quantity, demo_product.title from orders_orderitem join orders_order     on orders_orderitem.order_id = orders_order.id join demo_product on orders_orderitem.product_id = demo_product.id where orders_order.id=' +str(order.id)
 	cursor = connection.cursor()
	cursor.execute(sql)
        row = cursor.fetchall()
	print(row)
	#Task : Email Notification dispatch
	order_created.delay(order.id)	
	return row
   
@task(name="send_mail_to_custormer")
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {} {},\n\nYou have successfully placed an order. Your order id is {}'.format(order.first_name,order.last_name, order.id)
    from_email = settings.EMAIL_HOST_USER
    to_email = [order.email]
    mail_sent = send_mail(
                            subject,
                            message,
                            from_email,
                            to_email,
                            fail_silently=False
                          )
    return mail_sent


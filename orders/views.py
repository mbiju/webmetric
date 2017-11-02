# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import process_order
import redis
import pickle
import dill
from django.conf import settings

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def order_create(request):
    #Put the Entire Cart object in the redis cache :
    cart = Cart(request)
    pickled_object = dill.dumps(cart)
    print("Pickled OUTPUT")
    print(pickled_object)    
    r.set('cart',pickled_object)
   
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        for value in process_order.delay(
            request.POST.get('first_name', ''),request.POST.get('last_name', ''),request.POST.get('email', ''),
                request.POST.get('address', ''),request.POST.get('postal_code', ''), request.POST.get('city', '')).get():

                # form.cleaned_data.get('first_name'),
                #                             form.cleaned_data.get('last_name'),
                #                             form.cleaned_data.get('email'), form.cleaned_data.get('address'),
                #                             form.cleaned_data.get('postal_code'), form.cleaned_data.get('city')):
                order_number = value[0]
                first_name = value[1]
                last_name = value[2]
                address = value[3]
                product_title = value[7]
                product_quantity  = value[6]
                product_price  = value[5]
	    
        r.delete("cart")
        cart= None
        for key in request.session.keys():
            del request.session[key]
	    return render(request,'orders/order_created.html',
                      {'title': product_title,
                       'quantity':product_quantity, 'price': product_price , 'order_number':order_number,
                       'first_name':first_name,'last_name':last_name, 'address': address,   })
    else:
	form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})
   


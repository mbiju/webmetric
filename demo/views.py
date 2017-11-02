# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from .models import Product
from cart.forms import CartAddProductForm

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        queryset = Product.objects.all()
        context['products'] = queryset
        return context


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context
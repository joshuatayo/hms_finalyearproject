from django.shortcuts import render
from app.models import Drug
from .cart import Cart

def add_to_cart(request,id):
    if request.method == 'POST':
        drug = Drug.objects.get(id=id)
        quantity = request.POST['quantity']
        if not quantity:
            quantity = 1

        cart = Cart(request)
        cart.add(drug,quantity)

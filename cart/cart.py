from django.conf import settings
from app.models import Drug
from decimal import Decimal

class Cart(object):
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self,drug,quantity):
        drug_id = str(drug.id)
        self.cart[drug_id] = {'quantity':quantity,'price':str(drug.price)}
        self.save()

    def save(self):
        self.session.modified = True

    def list(self):
        carts = []
        for drug_id in self.cart.keys():
            obj =  Drug.objects.get(id=drug_id)
            tmp_cart = {
                'id':drug_id,
                'obj':obj,
                'quantity':self.cart[drug_id]['quantity'],
                'price': Decimal(int(self.cart[drug_id]['quantity']) * float(obj.price))
            }
            carts.append(tmp_cart)
        return carts

    def get_total_price(self):
        return sum(Decimal(v['price']) for v in self.cart.values())

    def remove(self,id):
        drug_id = str(id)
        if drug_id in self.cart:
            del self.cart[drug_id]
            self.save()
    


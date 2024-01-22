import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from math import ceil
from . import keys
import stripe
# Create your views here.
stripe.api_key = keys.STRIPE_SECRET_KEY
endpoint_secret = keys.STRIPE_WEBHOOK_KEY


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "index.html", params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")
        myquery = Contact(name=name, email=email,
                          desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "we will get back to you soon..")
        return render(request, "contact.html")
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def blog(request):
    return render(request, "about.html")

def orders(request):
   return render(request, "orders.html")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/authenticate/login')

    if request.method == "POST":
        # host = request.get_host()

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1,
                       address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        # print(amount)
        Order.save()


# # PAYMENT INTEGRATION

        id = Order.order_id
        oid = str(id)+"ShopyCart"
        # param_dict = {

        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'currency':'inr'
        # }

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    "price_data": {
                        'currency':'inr',
                        'unit_amount': amount*100,
                        'product_data':{
                            'name': oid,
                            'id':id,
                        },
                    },
                    'quantity':1,
                },
            ],
        )

        mode = 'payment'
        success_url='https://127.0.0.1:8000/success'
        cancel_url='https://127.0.0.1:8000/cancel'
        return redirect(session.url, code=303)

    return render(request, 'checkout.html')

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )

    if session.payment_status == 'paid':
       line_item = session.line_items
       fulfill_order(line_item)

  # Passed signature verification
  return HttpResponse(status=200)

def fulfill_order(line_items):
  oid = line_items[0]["price_data"]["product_data"]["name"]
  order_id = line_items[0]["price_data"]["product_data"]["id"]
  amount_paid = line_items[0]["price_data"]["unit_amount"]

  order = Orders.objects.get(id = order_id)
  order.paymentstatus = 'paid'
  order.amountpaid = amount_paid
  order.oid = oid
  order.save()
  
  order_update = OrderUpdate(order_id=order_id, update_desc = "item has been placed", 
                            delivered = True, timestamp=datetime.date.today())
  order_update.save()

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/authenticate/login')
    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)
    rid = ""
    for i in items:
        # print(i.oid)
        # print(i.order_id)
        myid = i.oid
        rid = myid.replace("ShopyCart", "")
        # print(rid)
    status = OrderUpdate.objects.filter(order_id=int(rid))
    # for j in status:
    # print(j.update_desc)

    context = {"items": items, "status": status}
    # print(currentuser)
    return render(request, "profile.html", context)

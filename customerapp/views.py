import smtplib
from email.message import EmailMessage

from django.db.models import ExpressionWrapper, F, Sum, DecimalField, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from adminapp.models import tbl_subcategory, tbl_category, tbl_product, tbl_district, tbl_location
from customerapp.models import tbl_cart, Book, Payment
from footwearapp.models import tbl_login, tbl_customer
from django.views.decorators.cache import cache_control


def index(request):
    return render(request, 'customer/index.html')


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subcategoryview(request, id):
    subcategory = tbl_subcategory.objects.filter(categoryid=id)
    return render(request, "customer/viewsubcategory.html", {'subcategory': subcategory})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryview(request):
    category = tbl_category.objects.all()
    return render(request, "customer/viewcategory.html", {'category': category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productview(request, id):
    product = tbl_product.objects.filter(subcategoryid=id)
    return render(request, "customer/viewproduct.html", {'product': product})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductdetails(request, id):
    category = tbl_category.objects.all()
    product = tbl_product.objects.filter(productid=id).select_related('subcategoryid').first()
    cartcount = tbl_cart.objects.filter(customer=request.session['login_id'], status='cart').count()
    request.session['cartcount'] = cartcount
    return render(request, 'customer/viewproductdetails.html',
                  {'cartcount': cartcount, 'uname': request.session['username'], 'p': product, 'category': category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_buy(request, id):
    if request.method == "POST":
        if request.POST.get('cart') == "Add to Cart":

            # return HttpResponse(tbl_customer.objects.get(loginid__login_id=request.session['login_id']))
            qty = request.POST.get('qty')
            # return HttpResponse(id+" "+qty)
            cob = tbl_cart()
            cob.quantity = qty
            cob.customer = tbl_login.objects.get(login_id=request.session['login_id'])
            pr = tbl_product.objects.get(productid=id)
            cob.productid = pr
            cob.status = 'cart'
            # return HttpResponse(str(qty)+" "+pr.quantity+" "+)
            if int(qty) > int(pr.quantity):
                return HttpResponse("<script>alert('Stock Exceeds." + str(
                    pr.quantity) + " items in Stock..');window.location='/customerapp/productsdetails/" + id + "';</script>")
            else:
                # return HttpResponse("hai")
                cart = tbl_cart.objects.filter(productid=id, customer_id=request.session['login_id'],
                                               status='cart').values()
                if not cart.exists():
                    # return HttpResponse("hello")
                    cob.save()
                else:
                    for c in cart:
                        qty = int(qty) + int(c['quantity'])
                        tbl_cart.objects.filter(customer_id=request.session['login_id'],
                                                status='cart',
                                                productid=id).update(
                            quantity=qty,
                        )
                message = "<script>alert('Product Added to Cart" + str(
                    pr.quantity) + " items in Stock..');window.location='/customer/cartdetails/""';</script>"
                return HttpResponse(message)
        else:

            qty = request.POST.get('qty')
            pr = tbl_product.objects.get(productid=id)
            if int(qty) > int(pr.quantity):
                message = "<script>alert('Stock Exceeds." + str(
                    pr.stock) + " items in Stock..');window.location='/customer/categoryview/""';</script>"
                return HttpResponse(message)
            else:
                request.session['grand_total'] = int(qty) * pr.price
                cob = tbl_cart()
                cob.quantity = int(qty)
                cob.status = "buy"
                # return HttpResponse(request.session['login_id'])
                cob.customer = tbl_login.objects.get(login_id=request.session['login_id'])
                pr = tbl_product.objects.get(productid=id)
                cob.productid = pr
                cob.save()
                request.session['cartid'] = cob.cartid
                request.session['pid'] = id
                customer = tbl_login.objects.get(login_id=request.session['login_id'])
                return render(request, 'Customer/payment.html',
                              {'grand_total': request.session['grand_total'], 'customer': customer, 'qty': qty,

                               'cartcount': request.session['cartcount'], "msg": "buynow"})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cartdetails(request):
    # return HttpResponse(request.session['loginid'])
    cart = tbl_cart.objects.filter(
        status='cart',
        customer_id=request.session['login_id']
    )

    grand_total = tbl_cart.objects.filter(
        status='cart',
        customer_id=request.session['login_id'],
        quantity__lte=F('productid__quantity')
    ).aggregate(
        grand_total=Sum(
            ExpressionWrapper(
                F('quantity') * F('productid__price'),
                output_field=DecimalField()
            )
        )
    )['grand_total']
    # return HttpResponse(grand_total)
    cartcount = tbl_cart.objects.filter(customer_id=request.session['login_id'], status='cart').count()

    request.session['cartcount'] = cartcount
    request.session['grand_total'] = str(grand_total)
    p_count = tbl_cart.objects.filter(customer_id=request.session['login_id'], status='cart',
                                      quantity__lte=F('productid__quantity')).count()
    # return HttpResponse(str(p_count))
    return render(request, 'Customer/cartdetails.html', {'p_count': p_count, 'grand_total': grand_total, 'cart': cart,
                                                         'username': request.session['username'],
                                                         'cartcount': request.session['cartcount']})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def removecartitem(request, id):
    data = tbl_cart.objects.get(cartid=id)
    data.delete()
    return HttpResponse("<script>alert('successfully deleted');window.location='/customer/cartdetails'</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateqty(request):
    qty = request.POST.get("qty")
    cid = request.POST.get("cid")
    cob = tbl_cart.objects.get(cartid=cid)
    cob.quantity = qty
    cob.save()
    i = 1
    # Print the SQL query generated by Django
    return JsonResponse(i, safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment(request):
    if request.method == "POST":
        grandtotal = request.POST.get('gtotal')

        return render(request, 'Customer/payment.html',
                      {'grand_total': grandtotal, 'cartcount': request.session['cartcount'],
                       'username': request.session['username']})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def placeorder(request):
    id = request.session['login_id']
    customer = tbl_customer.objects.get(loginid=id)
    cuemail = customer.email
    if request.method == "POST":
        bob = Book()
        bob.TotalAmount = float(request.POST.get('grand_total'))
        bob.customer = tbl_login.objects.get(login_id=request.session['login_id'])
        bob.status = 'Booked'
        max_bill = Book.objects.aggregate(max_value=Max('billno'))['max_value']
        # Check if there are existing bills
        if max_bill is not None:
            new_billno = max_bill + 1
        else:
            new_billno = 1654

        bob.billno = new_billno
        # return HttpResponse(bob.billno)
        bob.save()
        pob = Payment()
        pob.status = "paid"
        pob.TotalAmount = float(request.POST.get('grand_total'))
        pob.deliveryaddress = (request.POST.get('deliveryaddress'))
        pob.book = bob
        pob.save()
        msg = EmailMessage()
        msg.set_content('Your order is placed...Thank you for Choosing us')
        msg['Subject'] = "Payment Report"
        msg['From'] = 'allanshyson5@gmail.com'
        msg['To'] = cuemail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('allanshyson5@gmail.com', 'xngb posv jmcx igiy')
            smtp.send_message(msg)

        if 'cartid' in request.session:

            cob = tbl_cart.objects.get(cartid=int(request.session['cartid']))
            cob.billno = new_billno
            cob.status = 'Booked'
            cob.save()
            del request.session['cartid']
            id = request.session['pid']
            del request.session['pid']
            product = tbl_cart.objects.filter(billno=new_billno).select_related('productid')
            for p in product:
                quantity = int(p.productid.quantity) - int(p.quantity)
                tbl_product.objects.filter(productid=p.productid.productid).update(
                    quantity=quantity
                )
            return HttpResponse(
                "<script>alert('Successfully Ordered...');window.location='/customer/categoryview/" "';</script>")
        else:
            tbl_cart.objects.filter(customer=request.session['login_id'], status='cart').update(
                billno=new_billno,
                status='Booked'
            )
            product = tbl_cart.objects.filter(billno=new_billno).select_related('productid')
            for p in product:
                quantity = int(p.productid.quantity) - int(p.quantity)
                tbl_product.objects.filter(productid=p.productid.productid).update(
                    quantity=quantity
                )
            cartcount = tbl_cart.objects.filter(customer=request.session['login_id'], status='cart').count()
            request.session['cartcount'] = cartcount
            return HttpResponse("<script>alert('Successfully Ordered...Your Bill No is" + str(
                new_billno) + "');window.location='../cartdetails/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def index(request):
    if 'login_id' in request.session:
        logid = request.session.get('login_id')
        logname = request.session.get('username')
        if logid:
            return render(request, "customer/index.html", {'login_id': logid, 'username': logname})
        else:
            return HttpResponse(
                 "<script>alert('Logout Successfull');window.location='/login';</script>")
    else:
        return HttpResponse(
                     "<script>alert('login');window.location='/login';</script>")



def logout(request):
    if "login_id" in request.session:
        del request.session["login_id"]
        del request.session['username']
    return redirect(index)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customerprofile(request):
    id = request.session['login_id']
    customer = tbl_customer.objects.get(loginid=id)
    idm = customer.customerid
    data = tbl_customer.objects.filter(customerid=idm)
    # name=data.customername
    return render(request, 'customer/customerprofile.html', {'data': data})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit(request, id):
    if request.method == "POST":
        bid = request.session.get('login_id')
        log = tbl_login.objects.get(login_id=bid)
        cob = tbl_customer.objects.get(customerid=id)
        cob.customername = request.POST.get('customername')
        cob.housename = request.POST.get('house')
        cob.email = request.POST.get('email')
        cob.phno = request.POST.get('phone')
        cob.pincode = request.POST.get('pin')
        cob.locationid = tbl_location.objects.get(locationid=request.POST.get('location'))
        cob.loginid
        cob.save()
        log.username = request.POST.get('username')
        log.password = request.POST.get('password')
        log.save()
        return HttpResponse("<script>alert('Updated');window.location ='/customer/index';</script>")
    else:
        district = tbl_district.objects.all()
        custobj = tbl_customer.objects.get(customerid=id)
        return render(request, 'customer/editprofile.html', {'da': custobj, 'district': district})


def selectlocation(request):
    did = int(request.POST.get("did"))
    # return HttpResponse(did)
    location = tbl_location.objects.filter(districtid=did).values()
    return JsonResponse(list(location), safe=False)


from django.shortcuts import render, HttpResponse
from .models import tbl_login


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        password = request.POST.get("password")
        newpwd = request.POST.get("newpwd")
        connewpwd = request.POST.get("connewpwd")

        if tbl_login.objects.filter(username=uname, password=password).exists():
            lo = tbl_login.objects.get(username=uname, password=password)

            if newpwd == connewpwd:
                lo.password = newpwd
                lo.save()
                return HttpResponse(
                    "<script>alert('Successfully updated!!');window.location='/customer/index/'</script>")
            else:
                return HttpResponse(
                    "<script>alert('Password Mismatch!!');window.location='/Customerapp/changepassword'</script>")
        else:
            return HttpResponse(
                "<script>alert('Invalid Username or Password!!');window.location='/Customerapp/changepassword'</script>")

    return render(request, "Customer/changepassword.html")

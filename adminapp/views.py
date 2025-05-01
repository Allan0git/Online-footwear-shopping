import smtplib
from email.message import EmailMessage

from django.db.models import Count, Sum, F, ExpressionWrapper
from django.forms import DecimalField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from adminapp.models import tbl_district, tbl_location, tbl_category, tbl_subcategory, tbl_product
from customerapp.models import tbl_cart, Book, Payment
from footwearapp.models import tbl_customer, tbl_login
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import View
import xlwt
import datetime


def index(request):
    return render(request, 'Admin/index.html')


# DISTRICT
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtreg(request):
    if request.method == "POST":
        districtname = request.POST.get('districtname')
        districtobj = tbl_district()
        if tbl_district.objects.filter(districtname=districtname).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/Admin/districtreg'</script>")
        districtobj.districtname = districtname
        districtobj.save()
        return HttpResponse(
            "<script>alert('Sucessfully Registerted');window.location='/Admin/districtreg'</script>")
    else:
        district = tbl_district.objects.all()
        return render(request, 'Admin/districtreg.html', {'district': district})


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editdistrict(request, id):
    if request.method == "POST":
        districtname = request.POST.get('districtname')
        districtobj = tbl_district.objects.get(districtid=id)
        districtobj.districtname = districtname
        districtobj.save()
        return districtview(request)
    else:
        districtobj = tbl_district.objects.get(districtid=id)
        return render(request, 'Admin/editdistrict.html', {'district': districtobj})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedistrict(request, id):
    districtobj = tbl_district.objects.get(districtid=id)
    districtobj.delete()
    return districtview(request)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtview(request):
    district = tbl_district.objects.all()
    return render(request, 'Admin/districtreg.html', {'district': district})


# LOCATION
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationreg(request):
    if request.method == "POST":
        data = tbl_location()
        data.locationname = request.POST.get('locationname')
        if tbl_location.objects.filter(locationname=request.POST.get('locationname')).exists():
            return HttpResponse("<script>alert('Already exists');window.location='/Admin/locationreg';</script>")
        else:
            data.districtid = tbl_district.objects.get(districtid=request.POST.get('districtname'))
            data.save()
            return HttpResponse("<script>alert('successfully added');window.location='/Admin/locationreg';</script>")
    location = tbl_location.objects.all()
    district = tbl_district.objects.all()
    return render(request, 'Admin/locationreg.html', {'location': location, 'district': district})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewlocation(request):
    location = tbl_location.objects.all()
    district = tbl_district.objects.all()
    return render(request, "admin/viewlocation.html", {'location': location, 'district': district})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editlocation(request, id):
    if request.method == 'POST':
        locationname = request.POST.get('locationname')
        loc = tbl_location.objects.get(locationid=id)
        loc.locationname = locationname
        loc.save()
        return viewlocation(request)
    loc = tbl_location.objects.get(locationid=id)
    return render(request, "Admin/editlocation.html", {'loc': loc})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletelocation(request, id):
    data = tbl_location.objects.get(locationid=id)
    data.delete()
    return HttpResponse("<script>alert('successfully deleted');window.location='/Admin/locationreg'</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filllocation(request):
    did = int(request.POST.get("did"))
    # return HttpResponse(did)
    location = tbl_location.objects.filter(districtid=did).values()
    return JsonResponse(list(location), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewlocation(request):
    location = tbl_location.objects.all()
    district = tbl_district.objects.all()
    return render(request, "Admin/viewlocation.html", {'location': location, 'district': district})


# CATEGORY

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryreg(request):
    if request.method == 'POST':
        name = request.POST.get('categoryname')
        if len(request.FILES) != 0:
            cimage = request.FILES['image']
        else:
            cimage = 'images/default.jpeg'
        data = tbl_category()
        data.categoryname = name
        data.image = cimage
        data.save()
        return HttpResponse("<script>alert('Inserted..');window.location ='/Admin/categoryreg';</script>")
    else:
        category = tbl_category.objects.all()
        return render(request, "Admin/categoryreg.html", {'category': category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcategory(request, id):
    if request.method == "POST":
        cat = tbl_category.objects.get(categoryid=id)
        cat.categoryname = request.POST.get('categoryname')
        if len(request.FILES) == 0:
            cat.image = request.POST.get('oldimg')
        else:
            cat.image = request.FILES['image']
        cat.save()
        return HttpResponse("<script>alert('successfully updated');window.location='/Admin/categoryreg'</script>")
    else:
        category = tbl_category.objects.get(categoryid=id)
        return render(request, 'admin/editcategory.html', {'cat': category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecategory(request, id):
    cat = tbl_category.objects.get(categoryid=id)
    cat.delete()
    return HttpResponse("<script>alert('successfully deleted');window.location='/Admin/categoryreg'</script>")


# Subcategory
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subcategoryreg(request):
    if request.method == "POST":
        data = tbl_subcategory()
        data.subcategoryname = request.POST.get('subcategoryname')
        if tbl_subcategory.objects.filter(subcategoryname=request.POST.get('subcategoryname')).exists():
            return HttpResponse("<script>alert('Already exists');window.location='/Admin/subcategoryreg';</script>")
        else:
            if len(request.FILES) != 0:
                cimage = request.FILES['image']
            else:
                cimage = 'images/default.jpeg'
            data.categoryid = tbl_category.objects.get(categoryid=request.POST.get('categoryname'))
            data.image = cimage
            data.save()
            return HttpResponse("<script>alert('successfully added');window.location='/Admin/subcategoryreg';</script>")
    subcategory = tbl_subcategory.objects.all()
    category = tbl_category.objects.all()
    return render(request, 'Admin/subcategoryreg.html', {'subcategory': subcategory, 'category': category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewsubcategory(request):
    subcategory = tbl_subcategory.objects.all()
    category = tbl_category.objects.all()
    return render(request, "Admin/viewsubcategory.html", {'category': category, 'subcategory': subcategory})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillsubcategory(request):
    did = int(request.POST.get("did"))

    subcategory = tbl_subcategory.objects.filter(categoryid=did).values()

    return JsonResponse(list(subcategory), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editsubcategory(request, id):
    if request.method == "POST":
        loc = tbl_subcategory.objects.get(subcategoryid=id)
        loc.subcategoryname = request.POST.get('subcategoryname')
        if len(request.FILES) == 0:
            loc.image = request.POST.get('oldimg')
        else:
            loc.image = request.FILES['image']
        loc.save()
        return HttpResponse("<script>alert('successfully updated');window.location='/Admin/viewsubcategory'</script>")
    else:
        subcategory = tbl_subcategory.objects.get(subcategoryid=id)
        return render(request, 'admin/editsubcategory.html', {'loc': subcategory})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletesubcategory(request, id):
    data = tbl_subcategory.objects.get(subcategoryid=id)
    data.delete()
    return HttpResponse("<script>alert('successfully deleted');window.location='/Admin/subcategoryreg'</script>")


# PRODUCT


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productreg(request):
    if request.method == "POST":
        data = tbl_product()
        data.productname = request.POST.get('productname')
        if tbl_product.objects.filter(productname=request.POST.get('productname')).exists():
            return HttpResponse("<script>alert('Already exists');window.location='/Admin/productreg';</script>")
        else:
            if len(request.FILES) != 0:
                cimage = request.FILES['image']
            else:
                cimage = 'images/default.jpeg'
        data.subcategoryid = tbl_subcategory.objects.get(subcategoryid=request.POST.get('subcategoryname'))
        data.image = cimage
        data.description = request.POST.get('description')
        data.price = request.POST.get('price')
        data.quantity = request.POST.get('quantity')
        data.save()
        return HttpResponse("<script>alert('successfully added');window.location='/Admin/productreg';</script>")
    product = tbl_product.objects.all()
    subcategory = tbl_subcategory.objects.all()
    return render(request, 'Admin/productreg.html', {'product': product, 'subcategory': subcategory})


@never_cache
def viewproduct(request):
    product = tbl_product.objects.all()
    subcategory = tbl_subcategory.objects.all()
    return render(request, "Admin/viewproduct.html", {'subcategory': subcategory, 'product': product})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillproduct(request):
    did = int(request.POST.get("did"))
    # return JsonResponse(list(did))
    product = tbl_product.objects.filter(subcategoryid=did).values()
    return JsonResponse(list(product), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editproduct(request, id):
    if request.method == "POST":
        loc = tbl_product.objects.get(productid=id)
        loc.productname = request.POST.get('productname')
        if len(request.FILES) == 0:
            loc.image = request.POST.get('oldimg')
        else:
            loc.image = request.FILES['image']
        loc.description = request.POST.get('description')
        loc.price = request.POST.get('price')
        loc.quantity = request.POST.get('quantity')
        loc.save()
        return HttpResponse("<script>alert('successfully updated');window.location='/Admin/viewproduct'</script>")
    else:
        product = tbl_product.objects.get(productid=id)
        return render(request, 'admin/editproduct.html', {'loc': product})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteproduct(request, id):
    data = tbl_product.objects.get(productid=id)
    data.delete()
    return HttpResponse("<script>alert('successfully deleted');window.location='/Admin/productreg'</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if 'login_id' in request.session:
        logid = request.session.get('login_id')
        logname = request.session.get('username')
        if logid:
            return render(request, "admin/index.html", {'login_id': logid, 'username': logname})
        else:
            return HttpResponse(
                "<script>alert('Logout Successfull');window.location='/login';</script>")
    else:
        return HttpResponse(
            "<script>alert('logout');window.location='/login';</script>")


def logout(request):
    if "login_id" in request.session:
        del request.session["login_id"]
        del request.session['username']
        return redirect('/login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pie_chart(request):
    labels = []
    data = []

    queryset = tbl_cart.objects.values('productid__productname').annotate(total_customer=Count('productid'))
    for s in queryset:
        labels.append(s['productid__productname'])
        data.append(s['total_customer'])

    return render(request, 'Admin/piechartproduct.html', {
        'labels': labels,
        'data': data,
    })


def pie_chart2(request):
    labels = []
    data = []

    queryset = tbl_customer.objects.values('locationid__locationname').annotate(total_customer=Count('customerid'))
    for s in queryset:
        labels.append(s['locationid__locationname'])
        data.append(s['total_customer'])

    return render(request, 'Admin/piechartcustloc.html', {
        'labels': labels,
        'data': data,
    })


class ExportExcelcustomer(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customerlist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Customer Name', 'House Name', 'Contact No ', 'EmailId ', 'PinCode']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tbl_customer.objects.all().values_list('customername', 'housename', 'phno', 'email', 'pincode')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


from datetime import datetime  # Import the datetime class explicitly
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Count
import xlwt


# Make sure to replace '.models' with the actual path to your Book model

class ExportExcelDatewiseReport(View):
    def get(self, request):
        return render(request, 'admin/datewise_report_form.html')

    def post(self, request):
        from_date_str = request.POST.get('fromDate')
        to_date_str = request.POST.get('toDate')

        if not from_date_str or not to_date_str:
            return HttpResponse("Both fromDate and toDate are required.")

        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="datewise_report.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Datewise Report')

        row_num = 0
        columns = ['Customer Name', 'Total Amount']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        queryset = Book.objects \
            .filter(booking_date__range=(from_date, to_date)) \
            .values('customer_id__tbl_customer__customername', 'TotalAmount') \
            .annotate()

        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row.values()):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


# def piechartbooking(request):
#     labels = []
#     data = []
#
#     # Assuming Tbl_booking has a ForeignKey to Table and Table has a ForeignKey to Restaurant
#     queryset = tbl_cart.objects.values('cartid__productid__tbl_product__productname').annotate(
#         total_booking=Count('BookId'))
#     for s in queryset:
#         labels.append(s.get('tableid_restaurantidtbl_restaurant_restaurantname',
#                             s.get('restaurantname', 'tableid_restaurantidtbl_restaurant_restaurantname')))
#
#         data.append(s['total_booking'])
#
#     return render(request, 'admin/piechartrestaurantwisebooking.html', {
#         'labels': labels,
#         'data': data,
#     })

class ExportExcelsubcategory(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="subcategorylist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Subcategory Name']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tbl_subcategory.objects.all().values_list('subcategoryname')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response

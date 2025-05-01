from django.urls import path
from . import views
from .views import ExportExcelcustomer, ExportExcelDatewiseReport, ExportExcelsubcategory

urlpatterns = [
    path('index/', views.index),

    path('districtreg/', views.districtreg, name='districtreg'),
    path('editdistrict/<id>/', views.editdistrict, name='editdistrict'),
    path('deletedistrict/<id>/', views.deletedistrict, name='deletedistrict'),

    path('locationreg/', views.locationreg, name='locationreg'),
    path('editlocation/<id>/', views.editlocation, name='editlocation'),
    path('deletelocation/<id>/', views.deletelocation, name='deletelocation'),
    path('viewlocation/', views.viewlocation, name="viewlocation"),
    path('filllocation/', views.filllocation, name="filllocation"),

    path('categoryreg/', views.categoryreg, name='categoryreg'),
    path('editcategory/<id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<id>/', views.deletecategory, name="deletecategory"),

    path('subcategoryreg/', views.subcategoryreg, name='subcategoryreg'),
    path('editsubcategory/<id>/', views.editsubcategory, name='editsubcategory'),
    path('deletesubcategory/<id>/', views.deletesubcategory, name='deletesubcategory'),
    path('viewsubcategory/', views.viewsubcategory, name="viewsubcategory"),
    path('fillsubcategory/', views.fillsubcategory, name="fillsubcategory"),

    path('productreg/', views.productreg, name='productreg'),
    path('editproduct/<id>/', views.editproduct, name='editproduct'),
    path('deleteproduct/<id>/', views.deleteproduct, name='deleteproduct'),
    path('viewproduct/', views.viewproduct, name="viewproduct"),
    path('fillproduct/', views.fillproduct, name="fillproduct"),
    path('piechartproduct/', views.pie_chart, name="piechartproduct"),
    path('piechartcustloc/', views.pie_chart2, name="piechartcustloc"),
    path('logout/', views.logout, name='logout'),
    path('export_excel/', ExportExcelcustomer.as_view(), name='export_excel'),
    path('ExportExcelDatewiseReport/', ExportExcelDatewiseReport.as_view(), name='ExportExcelDatewiseReport'),
    path('export_excel2/', ExportExcelsubcategory.as_view(), name='export_excel2'),


]

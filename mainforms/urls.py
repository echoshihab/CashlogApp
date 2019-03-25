from django.urls import path
from . import views

urlpatterns = [
    path('', views.cform, name='mainpage'),
    path('cashlog/', views.clogFormView),
    path('patientpay/', views.ptpayFormView, name='patientpay'),
    # CASHLOG REPORTS edit pages
    # reporteditview without parameter shows last hundred entries with edit
    # button
    path('reportedit/', views.reporteditView, name='reportedit'),
    # reporteditview with parameter shows the one entry with update form
    path('<int:parameter>/reportedit/',
         views.reporteditView, name='reportitemedit'),
    # this view processes the update form and renders success page
    path('<int:parameter>/clogitemupdate/',
         views.clogitemupdateView, name='clogItemEdit'),
    # PATIENTPAY REPORTS edit pages
    # resultViewPtpayEdit without parameters shows last hundred entries with
    # edit button
    path('ptpayedit/', views.resultViewPtpayEdit, name='ptpayedit'),
    # resultViewPtpayEdit with parameter shows the one entry with update form
    path('<int:parameter>/ptpayedit/',
         views.resultViewPtpayEdit, name='ptpayitemedit'),
    # resultViewPtpayEdit with parameter shows the one entry with update form
    path('<int:parameter>/ptpayitemedit/',
         views.ptpayItemEditView, name='ptpayItemSubmit'),
    # base report pages below
    path('reportclog/', views.resultViewClog, name='reportclog'),
    path('<parameter>/reportclog/', views.resultViewClog,
         name='reportclog'),  # parameter contains location
    path('reportptpay/', views.resultViewPtpay, name='reportptpay'),
    path('<parameter>/reportptpay/', views.resultViewPtpay,
         name='reportptpay'),  # parameter contains location
    path('superuser/', views.superUserview, name='superuser'),
    # delete item view below
    path('deleteitem', views.deleteView, name='delete'),  # for patientpay
    path('deleteitem-cashlog', views.deleteViewCashlog,
         name='deleteitem-cashlog'),  # for cashlog
    # audit- audit trail for deleted items below
    path('audit', views.auditView, name='audit')


]

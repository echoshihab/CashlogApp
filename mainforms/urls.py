from django.urls import path
from . import views

urlpatterns = [
    path('', views.cform),
    path('cashlog/', views.clogFormView),
    path('patientpay/', views.ptpayFormView, name='patientpay'),
    path('reportedit/', views.reporteditView, name='reportedit'),
    path('reportclog/', views.resultViewClog, name='reportclog'),
    path('<parameter>/reportclog/', views.resultViewClog, name='reportclog'),
    path('reportptpay/', views.resultViewPtpay, name='reportptpay'),
    path('<parameter>/reportptpay/', views.resultViewPtpay, name='reportptpay'),
    path('<int:parameter>/reportedit/', views.reporteditView, name='reportitemedit'),
    path('<int:parameter>/clogitemupdate/', views.clogitemupdateView, name= 'clogItemEdit'),
    path('superuser/', views.superUserview, name='superuser')


]

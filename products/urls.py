from django.urls import path
from . import views


urlpatterns = [
    path('', views.products, name='products'),
    path('apps/', views.applications, name='applications'),
    path('progcodes/', views.programme_codes, name='progcodes'),
    path('progcode<int:id>/', views.progCode_i, name='progCode_i'),
    path('app<int:id>/', views.app_i, name='app_i'),
    path('download<str:prod><int:id>/', views.download_prod, name='download'),
    path('purchase/<str:gate>', views.purchase_cart_items, name='makePurchase'),
    path('verifypurchaseirr/', views.verify_purchase_irr, name='verifyPurchaseIRR'),
    path('verifypurchasebtc/', views.verify_purchase_btc, name='verifyPurchaseBTC'),
    path('purchaseresultbtc/<str:success>',
         views.purchase_result_btc, name='purchaseresultBTC'),
]

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import ProgrammeCode, Application
from django.utils.translation import gettext as _
import requests as req
from django.conf import settings
import json
# Create your views here.


def products(request):
    return render(request, 'products/products.html', {
        'header': _('Products'),
        'title': _('Products')
    })


def applications(request):
    AllApplications = Application.objects.all().order_by('name')
    data = {
        'header': _('Applications'),
        'AllApplications': AllApplications,
        'title': _('Products')
    }
    if request.user.is_authenticated:
        userPurchasedApps = list(request.user.purchasedApps.all())
        data['purchasedApps'] = [app.id for app in userPurchasedApps]
        appsInUserCart = list(request.user.cartItems.appsSection.all())
        data['appsInUserCart'] = [app.id for app in appsInUserCart]
    return render(request, 'products/products.html', data)


def programme_codes(request):
    AllProgCodes = ProgrammeCode.objects.all().order_by('name')
    data = {
        'header': _('Programme codes'),
        'AllProgCodes': AllProgCodes,
        'title': _('Products')
    }
    if request.user.is_authenticated:
        userPurchasedProgCodes = list(request.user.purchasedProgCodes.all())
        data['purchasedProgCodes'] = [
            progCode.id for progCode in userPurchasedProgCodes]
        codesInUserCart = list(request.user.cartItems.codeProgsSection.all())
        data['codesInUserCart'] = [code.id for code in codesInUserCart]
    return render(request, 'products/products.html', data)


def progCode_i(request, id):
    progCode_i = ProgrammeCode.objects.get(id=id)
    if request.user.is_authenticated:
        codeIsPurchased = id in [item.id for item in list(
            request.user.purchasedProgCodes.all())]
    else:
        codeIsPurchased = False
    return render(request, 'products/progCodesDetail.html', {
        'progCode_i': progCode_i,
        'header': _('Code'),
        'title': _('Products'),
        'codeIsPurchased': codeIsPurchased
    })


def app_i(request, id):
    app_i = Application.objects.get(id=id)
    if request.user.is_authenticated:
        appIsPurchased = id in [item.id for item in list(
            request.user.purchasedApps.all())]
    else:
        appIsPurchased = False
    return render(request, 'products/appsDetail.html', {
        'app_i': app_i,
        'header': _('App'),
        'title': _('Products'),
        'appIsPurchased': appIsPurchased
    })


def purchase_cart_items(request, gate='IRR'):
    if request.user.is_authenticated:
        if gate == 'IRR':
            PayGate = apply_purchase(request)
        elif gate == 'BTC':
            PayGate = apply_purchase_crypto(request)
        return PayGate

    return redirect(reverse('login'))


def apply_purchase_crypto(request):
    SecretKey = settings.SECRET_KEY
    status = req.get(
        f'https://plisio.net/api/v1/operations?api_key={SecretKey}')
    return status


def apply_purchase(request):
    # return 0
    userCart = request.user.cartItems
    appsInCart = list(userCart.appsSection.all())
    codesInCart = list(userCart.codeProgsSection.all())
    description = ''
    for item in appsInCart:
        description += f"|{_('Buy')}:{item.name}|\n"
    for item in codesInCart:
        description += f"|{_('Buy')}:{item.name}|_\n"

    ZarinpalRequestURL = "https://api.zarinpal.com/pg/v4/payment/request.json"
    ZarinpalVerifyURL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    ZarinpalStartpayURL = "https://www.zarinpal.com/pg/StartPay"

    callback_url = f"{settings.BASE_URL}/products/verifypurchaseirr"
    # callback_url = f"{settings.BASE_URL_MAIN}/products/verifypurchase"
    data = {
        'merchant_id': settings.MERCHANT,
        'amount': int(userCart.totalPrice * 10),
        'description': description,
        'callback_url': callback_url,
        # 'MerchantID': settings.MERCHANT,
        # 'Amount': int(userCart.totalPrice * 10),
        # 'Description': description,
        # 'CallbackURL': callback_url,
        # 'metadata': {'email': request.user.email}
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json',
               'content-length': str(len(data))}
    res = req.post(ZarinpalRequestURL, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()
        if response['data']['code'] == 100:
            url = f"{ZarinpalStartpayURL}/{response['data']['authority']}"
            return redirect(url)
    return {
        'success': False
    }


def verify_purchase_irr(request):
    PayResult = request.GET
    if PayResult['Status'] == 'OK':
        userCart = request.user.cartItems
        appsInCart = list(userCart.appsSection.all())
        codesInCart = list(userCart.codeProgsSection.all())
        for item in appsInCart:
            request.user.purchasedApps.add(item.id)
        for item in codesInCart:
            request.user.purchasedProgCodes.add(item.id)
        request.user.cartItems.appsSection.clear()
        request.user.cartItems.codeProgsSection.clear()
        return redirect(reverse('profile'))
    return redirect(reverse('cart'))


def verify_purchase_btc(request):
    return 0


def purchase_result_btc(request, success):
    success = success.lower()
    if success == 'yes':
        return 0
    return 0


def download_prod(request, prod, id):
    if request.user.is_authenticated:
        if prod == 'app' and id in [item.id for item in list(request.user.purchasedApps.all())]:
            docFile = Application.objects.get(id=id)
            # ,content_type='application/text')
            response = HttpResponse(docFile.sourceFile)
            response['Content-Disposition'] =\
                f"attachment; filename=_{docFile.sourceFile.name}"
            return response
        elif prod == 'code' and id in [item.id for item in list(request.user.purchasedProgCodes.all())]:
            docFile = ProgrammeCode.objects.get(id=id)
            # ,content_type='application/text')
            response = HttpResponse(docFile.sourceFile)
            response['Content-Disposition'] =\
                f"attachment; filename=__{docFile.sourceFile.name}"
            return response
        else:
            pass
    else:
        return redirect(reverse('login'))

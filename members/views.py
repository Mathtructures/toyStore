from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _
from .models import Member
from products.models import Application, ProgrammeCode
from hashlib import sha256
from datetime import datetime
# from django.core.serializers import serialize
# Create your views here.


usernameForbidAscii = list(range(32, 48)) + list(range(58, 65)) +\
    list(range(91, 95)) + [96] + list(range(123, 128))
usernameForbidChars = [chr(asc) for asc in usernameForbidAscii]
usernameForbidChars += 'آ ا ب پ ت ث ج چ ح خ د ذ ر ز ش س ص ض ط ظ ع غ ف ق گ ک ل م ن و ه ی'.split(
    ' ')


def user_cart(request):
    if request.user.is_authenticated:
        totalPrice = request.user.cartItems.totalPrice
        userCart = request.user.cartItems
        allProdsInCart = {
            'apps': [],
            'codes': [],
        }
        for app in list(userCart.appsSection.all()):
            allProdsInCart['apps'].append(app)
        for code in list(userCart.codeProgsSection.all()):
            allProdsInCart['codes'].append(code)
        response = render(request, 'members/userCart.html',
                          {'allProdsInCart': allProdsInCart,
                           'totalPrice': totalPrice,
                           'title': _('Cart'),
                           'header': _('Cart')})
    else:
        response = redirect(reverse('login'))
    return response


def cart_operation(request, type, id, action, doRedirect=0):
    response = {}
    if request.user.is_authenticated:
        if not len(list(request.user.cartItems.appsSection.all()))\
                and not len(list(request.user.cartItems.codeProgsSection.all())):
            request.user.cartItems.totalPrice = 0
            request.user.cartItems.save()

        if type == 'app':
            item = Application.objects.get(id=id)
            itemIsInCart = item in list(
                request.user.cartItems.appsSection.all())
        elif type == 'code':
            item = ProgrammeCode.objects.get(id=id)
            itemIsInCart = item in list(
                request.user.cartItems.codeProgsSection.all())
        else:
            pass

        if action == 'add':
            if not itemIsInCart:
                response['respMessage'] = _('Item is added to your cart')
                if type == 'app':
                    request.user.cartItems.appsSection.add(item)
                    request.user.cartItems.totalPrice += item.price

                elif type == 'code':
                    request.user.cartItems.codeProgsSection.add(item)
                    request.user.cartItems.totalPrice += item.price
                else:
                    pass
            else:
                response['respMessage'] = _(
                    'This item has already been added to your cart.')
        elif action == 'remove':
            if itemIsInCart:
                response['respMessage'] = _('Item is removed from your cart')
                if type == 'app':
                    request.user.cartItems.appsSection.remove(item)
                    request.user.cartItems.totalPrice -= item.price
                elif type == 'code':
                    request.user.cartItems.codeProgsSection.remove(item)
                    request.user.cartItems.totalPrice -= item.price
                else:
                    pass
            else:
                response['respMessage'] = _(
                    'This item doesn\'t exist in your cart.')

    else:
        response['respMessage'] = _('Sorry! but are not authenticated!')
        response['respData'] = []
    request.user.cartItems.save()
    if doRedirect:
        return redirect(reverse('cart'))
    return JsonResponse(response)


def user_profile(request):
    if request.user.is_authenticated:
        purchasedApps = list(request.user.purchasedApps.all())
        purchasedCodes = list(request.user.purchasedProgCodes.all())

        return render(request, 'members/profile.html', {'header': _('Profile'),
                                                        'title': _('Profile'),
                                                        'purchasedApps': purchasedApps,
                                                        'purchasedCodes': purchasedCodes})
    else:
        return redirect(reverse('login'))


def logout_user(request):
    logout(request)
    return redirect(reverse('login'))


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        if username in list(Member.objects.values_list('username', flat=True)):
            member = Member.objects.get(username=username)
            if member.is_active:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse('profile'))
                else:
                    return render(request, 'members/login.html', {'header': _('Login'),
                                                                  'message': _('Invalid password'),
                                                                  'title': _('Login')})
            else:
                return render(request, 'members/login.html', {'header': _('Login'),
                                                              'message': _('Your account is not active!'),
                                                              'title': _('Login')})
        else:
            return render(request, 'members/login.html', {'header': _('Login'),
                                                          'message': _('Invalid username'),
                                                          'title': _('Login')})
    else:
        return render(request, 'members/login.html', {'header': _('Login'),
                                                      'title': _('Login')})


def signup_user(request):
    if request.method == 'POST':
        firstname = request.POST['first_Name']
        lastname = request.POST['last_Name']
        username = request.POST['user_Name'].lower()
        password = request.POST['passw1']
        # hashedPass = sha256(password.encode('utf_8')).hexdigest()
        email = request.POST['e_mail']
        cellphone = request.POST['cell_phone']
        if cellphone == '':
            cellphone = 000

        quote = request.POST['quote']
        member = Member.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname,
            cellphone=cellphone,
            quote=quote,
            registrationDate=datetime.now()
        )
        # login(request,member)
        member.is_active = False
        member.save()
        login(request, member)
        # user_activation(request, member, verifGeneratedCode)
        error = member.send_confirmation_mail()
        # return render(request, 'members/signup.html', {'header': _('Sign up'})
        if not error:
            response = user_activation(request, linkCheck=False)
        else:
            response = render(request, 'members/signup.html', {'header': _('Sign up'),
                                                               'title': _('Registration'),
                                                               'message': _('Verification email was not sent successfully!')})
        return response
    else:
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'members/signup.html', {'header': _('Sign up'),
                                                       'title': _('Registration')})


def is_user_text_valid(username):
    for ch in list(username):
        if ch in usernameForbidChars:
            return False
    return True


def is_user_valid(request):
    allUsernames = list(Member.objects.values_list('username', flat=True))
    username = request.GET.get('username')
    isUserTextValid = is_user_text_valid(username)
    if not isUserTextValid:
        isUservalidMsg = _(
            'Username should contain only numbers or english characters!')
    else:
        isUservalidMsg = ''

    if username:
        username = username.split('/')[0]
    if username in allUsernames:
        isUserUique = False
        isUniqueMsg = _('This username is already used!')
        messageColor = 'red'
    else:
        isUserUique = True
        isUniqueMsg = ''
        messageColor = 'rgb(0,100,100)'
    isUsernameValid = isUserUique and isUserTextValid
    data = {
        'result': isUsernameValid,
        'message': isUniqueMsg + ' ' + isUservalidMsg,
        'messageColor': messageColor
    }
    return JsonResponse(data)


def is_email_valid(request):
    allEmails = list(Member.objects.values_list('email', flat=True))
    email = request.GET.get('email')
    if email:
        email = email.split('/')[0]
    if email in allEmails:
        isEmailUique = False
        isUniqueMsg = _('This email is already used!')
        messageColor = 'red'
    else:
        isEmailUique = True
        isUniqueMsg = ''
        messageColor = 'blue'
    data = {
        'result': isEmailUique,
        'message': isUniqueMsg,
        'messageColor': messageColor

    }
    return JsonResponse(data)


def user_activation(request, linkCheck=True):
    if linkCheck:
        uid = int(request.GET['uid'])
        usernameInputHS = request.GET['userHS']
        member = Member.objects.get(id=uid)
        memberUser = member.username
        # usernameInputHS = sha256(usernameInput.encode('utf_8')).hexdigest()
        memberUserHS = sha256(memberUser.encode('utf_8')).hexdigest()
        if usernameInputHS == memberUserHS:
            member.is_active = True
            member.save()
            login(request, member)
        response = redirect(reverse('profile'))
        return response
    else:
        response = render(request, 'members/userActivation.html',
                          {'header': _('Activation'),
                              'message': f"{_('Dear')} {request.user.first_name}," +
                           f"{_(' a verification link is sent to')} {request.user.email}." +
                           f"{_(' Please click on it to activate.')}" +
                           f"{_('NOTE: <<PLEASE ALSO CHECK YOUR SPAM>>')}",
                           'title': _('Activation')})
        return response

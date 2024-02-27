from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
# from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from django.utils import translation


# Create your views here.
def homepage(request):
    # g = GeoIP2()
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')  
    # try:  
    #     location = g.city(ip)
    #     location_country = location["country_name"]
    #     location_city = location["city"]
    # except:
    #     location_country = False
    #     location_city = False
    return render(request, 'base/homepage.html',{
        'header': _('Homepage'),
        'title':'NUMERA',
    })


def change_lang(request, lang):
    request.LANGUAGE_CODE = lang
    translation.activate(lang)
    # request.session[LANGUAGE_SESSION_KEY] = request.LANGUAGE_CODE
    response = redirect(request.environ['HTTP_REFERER'])

    # url = request.get_full_path()
    # url = request.build_absolute_uri()
    # url = request.path_info
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from products.models import Application,ProgrammeCode
from django.core.serializers import serialize

# Create your views here.
def test(request):
    # id = request.GET['id']
    resp = {
        'num':18181818
    }
    # response = HttpResponse(resp,content_type="application/json")
    # response = JsonResponse(json.dumps(resp))
    response = JsonResponse(resp)
    return response

def returnApps(request):
    data = Application.objects.all()
    allApps = serialize("json", data)
    resp = {'allApps':allApps}
    return JsonResponse(resp)

def returnProgCodes(request):
    data = ProgrammeCode.objects.all()
    allProgs = serialize("json", data)
    resp = {'allApps':allProgs}
    return JsonResponse(resp)
    
    
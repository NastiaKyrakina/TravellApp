from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, QueryDict, HttpRequest

from UserProfile.models import UserExt, Country
from .models import House, HousePhoto, MAX_USER_HOUSES
from .form import HouseForm, PhotoForm, SearchHousesForm
from datetime import datetime
from Lib import FileFormats


def house_search_page(request):
    houses = House.objects.all()
    if 'user' in request.GET:
        user = get_object_or_404(UserExt, id=request.GET['user'])
        houses = House.objects.filter(owner=user)
    form_search = SearchHousesForm()
    houses = House.objects.multi_search(request.GET.dict())

    return render(request, 'HouseSerch/house_search.html',
                  {'houses': houses,
                   'form_search': form_search})


def house_page(request, house_id):
    house = get_object_or_404(House, id=house_id)
    is_owner = (request.user == house.owner)
    type = house.HOUSE_TYPE[house.type]
    data = {
        'type': type,
        'house': house,
        'is_owner': is_owner,

    }
    return render(request, 'HouseSerch/house_page.html', data)


def house_add_page(request):
    user = UserExt.objects.get(pk=request.user.pk)

    if user.house_set.count() == MAX_USER_HOUSES:
        return render(request, 'HouseSerch/limit_house.html', {user: user})

    errors_file_type = []

    if request.method == 'POST':
        form_house = HouseForm(request.POST)
        form_photo = PhotoForm(request.POST, request.FILES)
        if form_house.is_valid() and form_photo.is_valid():
            errors_file_type = FileFormats.handle_uploaded_file(request.FILES)
            if not errors_file_type:
                new_house = _home_save(request, form_house, user)
                return HttpResponseRedirect('/house/%s/' % new_house.id)
    else:
        form_house = HouseForm()
        form_photo = PhotoForm()

    return render(request,
                  'HouseSerch/add_house.html',
                  {'form_house': form_house,
                   'form_photo': form_photo,
                   'is_creating': True,
                   'errors_type': errors_file_type,
                   })


def _home_save(request, form_house, user):
    new_house = form_house.save(user)
    files = request.FILES.getlist('image', None)
    for file in files:
        new_house_photo = HousePhoto(house=new_house, image=file)
        new_house_photo.save()
    return new_house


def house_edit_page(request, house_id):
    house = get_object_or_404(House, id=house_id)
    user = UserExt.objects.get(pk=request.user.pk)

    if user != house.owner:
        return Http404

    errors_file_type = []
    if request.method == 'POST':
        form_house = HouseForm(request.POST, instance=house)
        form_photo = PhotoForm(request.POST, request.FILES)
        if form_house.is_valid() and form_photo.is_valid():
            errors_file_type = FileFormats.handle_uploaded_file(request.FILES)
            if not errors_file_type:
                new_house = _home_save(request, form_house, user)
                return HttpResponseRedirect('/house/%s/' % new_house.id)
    else:
        form_house = HouseForm(instance=house)
        form_photo = PhotoForm()

    return render(request,
                  'HouseSerch/add_house.html',
                  {'form_house': form_house,
                   'form_photo': form_photo,
                   'house': house,
                   'errors_type': errors_file_type,
                   })


def house_delete(request):
    if request.method == 'POST':
        house = House.objects.get(pk=int(QueryDict(request.body).get('housepk')))
        if request.user == house.owner:
            house.deleted = datetime.now()
            house.save()
            response_data = {}
            response_data['msg'] = 'Post was deleted.'
            return JsonResponse(response_data)

    return JsonResponse({"msg": "this isn't happening"})


def ajax_load_countries(request):
    if 'qcountry' in request.GET:
        qcountry = request.GET['qcountry']
        countries = Country.objects.filter(name__istartswith=qcountry)
        dictionaries = []

        for country in countries:
            country_json = {}
            country_json['label'] = country.name
            dictionaries.append(country_json)

        return JsonResponse({'dictionaries': dictionaries})
    return HttpResponse('false')

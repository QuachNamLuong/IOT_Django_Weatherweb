from django.forms import ValidationError
from django.shortcuts import render, redirect
import requests
from .models import City
from .models import CreateUserForm
from .forms import CityForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import json

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0576e071c691c65048556b66ee22d479&lang=vi"
    
    name = request.POST.get('name')
    form = CityForm()
    ############################################################################
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    ############################################################################
    if username is not None:
        if request.method == 'POST':
            name = request.POST.get('name')
            city_weather = requests.get(url.format(name)).json()
            if city_weather['cod'] != '404':
                city_name = {'name': city_weather['name'], 'username': username}
                form  = CityForm(city_name)
                if city_weather['cod'] == 200:
                    userCityExist = City.objects.filter(username=username).filter(name=city_name['name'])
                    if len(userCityExist) == 0:  
                        form.save()
            else:
                messages.error(request, 'None city')
   ############################################################################
    if username is not None:
        cities = City.objects.filter(username=username)
        weather_data = []
        for city in cities:
            city_weather = requests.get(url.format(city)).json()
            if city_weather['cod'] == 200:
                weather = {
                        'id': city.id,
                        'city' : city_weather['name'],
                        'temperature' : city_weather['main']['temp'],
                        'description' : city_weather['weather'][0]['description'],
                        'icon' : city_weather['weather'][0]['icon'],
                        'country': city_weather['sys']['country'],
                    }
                weather['temperature'] = round((weather['temperature'] - 32) / (9/5))
                weather_data.append(weather)
            else:
                City.objects.filter(name=city).delete()
        
        context = {'weather_data' : weather_data, 'form' : form}

        return render(request, 'weather/index.html', context)
    ############################################################################
    else:
        city_weather = requests.get(url.format(name)).json()
        if city_weather['cod'] == 200:
            weather = {
                    'city' : city_weather['name'],
                    'temperature' : city_weather['main']['temp'],
                    'description' : city_weather['weather'][0]['description'],
                    'icon' : city_weather['weather'][0]['icon'],
                    'country': city_weather['sys']['country'],
                }
            weather['temperature'] = round((weather['temperature'] - 32) / (9/5))

            context = {'weather_data' : [weather], 'form' : form}
            return render(request, 'weather/index.html', context)
        else:
            messages.error(request, 'None city')
        
        context = {'weather_data' : [], 'form' : form}
        return render(request, 'weather/index.html', context)
    ############################################################################

def register(request):
    formAuth = CreateUserForm()
    form = CityForm()
    
    if request.method == 'POST':
        formAuth = CreateUserForm(request.POST)
        if formAuth.is_valid():
            formAuth.save()
            return redirect('log-in')
        else:
            messages.error(request, 'check password, username and not accept only numberusername')
            context ={'form' : form,  'formAuth' : formAuth, 'prepareUp' : True}
            return render(request, 'weather/index.html', context)
    else:
        context ={'form' : form,  'formAuth' : formAuth, 'prepareUp' : True}
        return render(request, 'weather/index.html', context)

def loginAuth(request):
    form = CityForm()

    if request.user.is_authenticated:
        username = request.user.username
        context ={'form' : form,'prepareIn' : True}
        return render(request, 'weather/index.html', context)
        
    
    if request.method == 'POST':
        username =  request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again')
            context ={'form' : form, 'prepareIn' : True, 'isAuthor': request.user.is_authenticated} 
            return render(request, 'weather/index.html', context)
    else:
        context ={'form' : form, 'prepareIn' : True, 'isAuthor': request.user.is_authenticated}
        return render(request, 'weather/index.html', context)

def logOut(request):
    logout(request)
    return redirect('home')

@csrf_protect
def deleteCity(request):
    if request.user.is_authenticated:
        username = request.user.username
        id = json.loads(request.body.decode("utf-8"))
        City.objects.filter(id=id).filter(username=username).delete()
    return redirect('home')
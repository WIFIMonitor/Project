from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient

client = InfluxDBClient("localhost", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")

def index(request):
    return render(request, 'index.html')

def analytics(request):
    return render(request, 'analytics.html')

def timelapse(request):
    return render(request, 'timelapse.html')

def test(request):
    return render(request, 'bar_graphic.html')

def population_chart(request):
    labels = ['DETI', 'ESSUA', 'CANTINA', 'BIBLIOTECA']
    data = [100,110,560,900]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def myGraph(request):
    labels = ['DETI', 'ESSUA', 'CANTINA', 'BIBLIOTECA']
    data = [100, 110, 560, 900]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def get_buildings_count():
    res = client.query("select \"building\",\"clientsCount\" from clientsCount").raw['series'][0]["values"]
    



def get_building_names():
    res = client.query("show tag values from clientsCount with key = building").raw["series"][0]["values"]
    buildings = []
    for x in res:
        buildings.append(x[1])

    return buildings

get_buildings_count()
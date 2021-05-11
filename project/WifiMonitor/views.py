from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient

client = InfluxDBClient("localhost", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")

def index(request):
    return render(request, 'index.html')

def analytics(request):
    return render(request, 'analytics.html')

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
    building = client.query("show tag values from clientsCount with key = building")

    print(building[2])



get_buildings_count()
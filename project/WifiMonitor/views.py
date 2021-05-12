from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient

client = InfluxDBClient("***REMOVED***", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")

def heatmap(request):
    return render(request, 'heatmap.html')

def analytics(request):
    return render(request, 'analytics.html')

def timelapse(request):
    return render(request, 'timelapse.html')

def test(request):
    return render(request, 'bar_graphic.html')

def population_building_graph(request):
    count = get_buildings_count()
    labels = list(count.keys())
    data = list(count.values())

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def get_buildings_count():
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount\" from clientsCount where time >= now()-15m ").raw['series'][0]["values"]
        #print(res)
        count = {}

        #count(chave=edificio, value=n de pessoas no edificio)
        for sample in res:
            building = sample[1]
            if building not in count:
                count[building] = int(sample[2])
            else:
                count[building] = count[building] + int(sample[2])
    except:
        print('ERROR: getting data from DB')
        count = {}

    return count








def get_building_names():
    res = client.query("show tag values from clientsCount with key = building").raw["series"][0]["values"]
    buildings = []
    for x in res:
        buildings.append(x[1])

    return buildings

#get_building_names()
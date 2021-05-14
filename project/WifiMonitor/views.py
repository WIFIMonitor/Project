from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient

client = InfluxDBClient("***REMOVED***", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")
global prev_id
prev_id = 0
def heatmap(request):
    return render(request, 'heatmap.html')

def analytics(request):


    try:
        people_count = client.query("select sum(clientsCount) from clientsCount where time >= now()-15m ").raw['series'][0]["values"][0][1]
        residentials_people_count = client.query("select sum(\"clientsCount\") from clientsCount where \"building\"= \'ra\' and time >=now()-15m").raw['series'][0]["values"][0][1]
        campus_people_count = people_count - residentials_people_count
    except:
        people_count = "null"
        residentials_people_count = "null"
        campus_people_count = "null"

    tparams = {
        'people_count' : people_count,
        'residentials_people_count' : residentials_people_count,
        'campus_people_count' : campus_people_count
    }
    return render(request, 'analytics.html', tparams)

def timelapse(request):
    return render(request, 'timelapse.html')

def test(request):
    return render(request, 'line_graph.html')

def population_building_graph(request):
    count = get_buildings_count()
    labels = list(count.keys())
    data = list(count.values())

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
def specific_building(request):
    global prev_id
    buildings = dict(enumerate(get_building_names()))
    print(buildings)
    if request.method == "GET":  # carregar a pag
        id = 0
        building_name = "Choose your building"

    if request.method == "POST":
        id = request.POST["buildSelect"]
        building_name = buildings[int(id)]

    if (prev_id == id):
        building_name = "Choose your country"

    prev_id = id
    tparams = {
        'buildings': buildings,
        'default_message': building_name,
    }
    return render(request, 'specific_building.html', tparams)


    return render(request, 'specific_building.html')
def get_buildings_count():
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount\" from clientsCount where time >= now()-15m ").raw['series'][0]["values"]
        #print(res)
        count = {}

        #count(chave=edificio, value=n de pessoas no edificio)
        for sample in res:
            building = sample[1]
            if building == 'ra':
                continue
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
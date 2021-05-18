from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient
import re
import json


client = InfluxDBClient("***REMOVED***", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")
global prev_id
prev_id = 0

# load ap cooordinates into memory, so that we dont 
# have to read the excel file every time someone
# wants to check the heatmap
def load_ap_coords():
    people_count = client.query("select id,clientsCount from clientsCount where time >= now()-15m ").raw['series'][0]["values"]
    
    hash_coords = {}
    for line in people_count:
        hash_coords[line[1]] = line[2]

    coords = []
    f = open("WifiMonitor/static/fileCoords.txt","r")
    
    for line in f:
        info = line.split(",")
        
        dic = { "id" : info[0],
        "lat" : info[1],
        "lon" : info[2].strip('\n'),
        "people" : hash_coords[info[0]]
        }
        coords.append(dic)
 
    return coords
 
def index(request):
    return render(request, 'index.html')

def heatmap(request):
    ap_coordinates = load_ap_coords()
    params = {
    'api_key': 'AIzaSyA9M86-1yyuucibiNR-wh8kiboANAcUjuI',
    'data' : json.dumps(ap_coordinates)
    }
    
    return render(request, 'heatmap.html', params)

def overview(request):
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
    return render(request, 'overview.html', tparams)

def campus_distribution(request):
    return render(request, 'campus_distribution.html')

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

def specific_building(request, building=None):
    global prev_id
    buildings = dict(enumerate(get_building_names()))
    #print(buildings)
    if request.method == "GET":  # carregar a pag
        id = 0
        building_name = "Choose your building"

    if request.method == "POST":
        id = request.POST["buildSelect"]
        building_name = buildings[int(id)]

    if (prev_id == id):
        building_name = "Choose your building"

    prev_id = id
    tparams = {
        'buildings': buildings,
        'default_message': building_name,
    }
    return render(request, 'specific_building.html', tparams)

def line_graph(request, building = None):
    if(building != None):
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'"+building +"\' and time >=now()-24h GROUP BY time(15m)) group by time(1h)").raw['series'][0]["values"]
    print(values)
    labels = []
    data = []

    for sample in values:
        labels.append(sample[0][sample[0].find('T')+1 : -4])
        data.append(sample[1])


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

def get_building_lastday_population():
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

#get_building_names()

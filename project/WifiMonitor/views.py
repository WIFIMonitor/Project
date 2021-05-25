from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient
import plotly.express as px
import json
from datetime import datetime
from .forms import DateForm,IntentionForm
from .models import Departments
from django.db.models import F,Sum

client = InfluxDBClient("***REMOVED***", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")
global prev_id
prev_id = 0

def get_last_ts():
    # get the last timestamp value of the database
    return client.query("select last(clientsCount) from clientsCount").raw['series'][0]['values'][0][0]

# Get the date of the measures being displayed
timestamp = "Dia: "+get_last_ts().replace("T"," às ")[:-8]

# load ap cooordinates into memory, so that we dont 
# have to read the excel file every time someone
# wants to check the heatmap
def load_ap_coords():
    coords = {}
    f = open("WifiMonitor/static/fileCoords.txt","r")

    for line in f:
        info = line.split(",")
        dic = { 
        "lat" : info[1],
        "lon" : info[2].strip('\n'),
        "piso" : info[3] if info[3]!="None\n" else "Não Definido",
        }
        coords[info[0]] = dic
    
    f.close()
    return coords

coords = load_ap_coords()

def get_timelapse_dictionary(dataset,endtime,starttime,measure):
    # query values between last measurement, minus 15 minutes
    sq = "select id,clientsCount from clientsCount where time <=\'"+starttime+"m and time > \'" +endtime+"m" 
    # get the last 15m values, from the last value in DB, and not from now(), because CISCO PRIME can stop sending values
    try:
        people_count = client.query(sq).raw['series'][0]["values"]
    except:
        return
   
    for line in people_count:
        # only add to the timelapse points that have people conected, to not overload the array
        if line[2] != 0:
            if line[1] in coords:
                dic = {"id": line[1],
                        "lat": coords[line[1]]["lat"],
                        "lon":coords[line[1]]["lon"],
                        "piso":coords[line[1]]["piso"],
                        "people":line[2],
                        "measure":measure,
                        }     
                dataset.append(dic)
            else:
                continue

def get_heatmap_dictionary(timestamp):
    dataset = []
    # query values between last measurement, minus 15 minutes
    sq = "select id,clientsCount from clientsCount where time >=\'"+timestamp+"\' -15m" 
    # get the last 15m values, from the last value in DB, and not from now(), because CISCO PRIME can stop sending values
    try:
        people_count = client.query(sq).raw['series'][0]["values"]
    except:
        return
    for line in people_count:
        # only add to the timelapse points that have people conected, to not overload the array
        if line[2] != 0:
            if line[1] in coords:
                dic = {"id": line[1],
                        "lat": coords[line[1]]["lat"],
                        "lon":coords[line[1]]["lon"],
                        "piso":coords[line[1]]["piso"],
                        "people":line[2],
                        }     
                dataset.append(dic)
            else:
                continue

    return dataset

 
def index(request):
    return render(request, 'index.html')

def heatmap(request):
    date_form = DateForm(request.POST or None)
    intent_form = IntentionForm(request.POST or None)

    if(request.method=='POST'):
        if date_form.is_valid():
            start = date_form.cleaned_data.get('start')
            end = date_form.cleaned_data.get('end')
            
            start_time = datetime.strptime(str(start), "%Y-%m-%d").isoformat('T')
            end_time = datetime.strptime(str(end), "%Y-%m-%d").isoformat('T')
            
            #generate timelapse graph
            generateTimelapse(start_time,end_time)

        if intent_form.is_valid():
            try:
                depart = intent_form.cleaned_data.get('departs')
                # get people at the specified department
                people_at = Departments.objects.get(name=depart)
                # add 1
                people_at.people = F('people')+1
                #save
                people_at.save()
            except:
                print("Invalid choice")

    latestTS = get_last_ts()
    ap_values = get_heatmap_dictionary(latestTS)
    people_going_to_campus = Departments.objects.aggregate(Sum('people'))['people__sum']
    params = {
        'api_key': 'AIzaSyA9M86-1yyuucibiNR-wh8kiboANAcUjuI',
        'data': json.dumps(ap_values),
        'time': timestamp,
        'date_form': date_form,
        'intent_form': intent_form,
        'buildings': get_building_names(),
        'people_going': people_going_to_campus,
        }

    return render(request, 'heatmap.html', params)

def overview(request):
    latestTS = get_last_ts()
    try:
        people_count = client.query("select sum(clientsCount) from clientsCount where time >=\'"+latestTS+"\'-15m ").raw['series'][0]["values"][0][1]
        residentials_people_count = client.query("select sum(\"clientsCount\") from clientsCount where \"building\"= \'ra\' and time >=\'"+latestTS+"\'-15m").raw['series'][0]["values"][0][1]
        campus_people_count = people_count - residentials_people_count
    except:
        people_count = "null"
        residentials_people_count = "null"
        campus_people_count = "null"

    tparams = {
        'people_count' : people_count,
        'residentials_people_count' : residentials_people_count,
        'campus_people_count' : campus_people_count,
        'time':timestamp
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
        'time':timestamp
    }
    return render(request, 'specific_building.html', tparams)

def line_graph(request, building = None):
    latestTS = get_last_ts()
    if(building != None):
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'"+building +"\' and time >=\'"+latestTS+"\'-24h GROUP BY time(15m)) group by time(1h)").raw['series'][0]["values"]
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
    latestTS = get_last_ts()
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount\" from clientsCount where time >= \'"+latestTS+"\'-15m ").raw['series'][0]["values"]
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
    latestTS = get_last_ts()
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount\" from clientsCount where time >=\'"+latestTS+"\'-15m ").raw['series'][0]["values"]
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

def generateTimelapse(start_time,end_time):
    dataset = []
    latestTS = get_last_ts()
    # Generate 50 timelaspes. In the future it will be decided by the user input
    for x in range(1,10):
        try:
            # since we get values every 15 minutes, we need to now how many 15 minute measures we want
            sub1 = str(15*x)
            sub2 = str(15*(x-1))
            endtime = str(latestTS) + "\' -"+sub2
            starttime = str(latestTS) + "\' -"+sub1

            get_timelapse_dictionary(dataset,starttime,endtime,x)
        except Exception as e:
            print(e)
            continue

    fig = px.density_mapbox(dataset, lat='lat', lon='lon', z='people', radius=10,animation_frame='measure',
            center=dict(lat=40.63041451444991, lon=-8.65803098047244),
            zoom=15,
            mapbox_style="stamen-terrain",
            width=550,
            height=1100,
            color_continuous_scale= [
                    [0.0, "green"],
                    [0.3, "green"],
                    [0.5, "yellow"],
                    [0.7, "yellow"],
                    [0.9, "red"],
                    [1.0, "red"]],
            title= str(latestTS) + "- " + str((x*15)) + "m",
            range_color=(0,30), #max and min values for heatmap
               )

    fig.write_html("WifiMonitor/static/slider.html")

from django.http import JsonResponse
from django.shortcuts import render
from influxdb import InfluxDBClient
import plotly.express as px
import json
from datetime import datetime
from .forms import DateForm,IntentionForm,SpecificBuildingForm
from .models import Departments
from django.db.models import F,Sum
from numpy import random

client = InfluxDBClient("***REMOVED***", ***REMOVED***, "***REMOVED***", "***REMOVED***", "***REMOVED***")
global prev_id
prev_id = 0

def get_last_ts():
    # get the last timestamp value of the database
    return client.query("select last(clientsCount) from clientsCount").raw['series'][0]['values'][0][0]

# Get the date of the measures being displayed
timestamp = "from day: "+get_last_ts().replace("T"," at ")[:-8]

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

def get_heatmap_dictionary():
    latestTS = get_last_ts()
    dataset = []
    # query values between last measurement, minus 15 minutes
    sq = "select id,clientsCount from clientsCount where time >=\'"+latestTS+"\' -15m"
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
        # Check whether timelapse or intent form were submitted
        if 'timelapse_submit' in request.POST:
            if date_form.is_valid():
                start = date_form.cleaned_data.get('start')
                end = date_form.cleaned_data.get('end')

                start_time = datetime.strptime(str(start), "%Y-%m-%d").isoformat('T')
                end_time = datetime.strptime(str(end), "%Y-%m-%d").isoformat('T')

                #generate timelapse graph
                generateTimelapse(start_time,end_time)

        if 'intent_submit' in request.POST:
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

    ap_values = get_heatmap_dictionary()
    people_going_to_campus = Departments.objects.aggregate(Sum('people'))['people__sum']
    params = {
        'api_key': 'AIzaSyA9M86-1yyuucibiNR-wh8kiboANAcUjuI',
        'data': json.dumps(ap_values),
        'time': timestamp,
        'date_form': date_form,
        'intent_form': intent_form,
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

    data2 = []
    for i in range(1, 53):
        data2.append(random.randint(25))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data2': data2,
    })

def specific_building(request, building=None):
    global prev_id
    specific_build_form = SpecificBuildingForm(request.POST or None) 
    
    if(request.method=='POST'):
        if specific_build_form.is_valid():
            building = specific_build_form.cleaned_data.get('departs')
            line_graph(request,building) 

    prev_id = id
    tparams = {
        'buildings': "Building",
        'default_message': "Building",
        'time': timestamp,
        'specific_building_form': specific_build_form,
    }
    return render(request, 'specific_building.html', tparams)

def specific_building_monthly_users(request, building=None):
    global prev_id
    buildings = dict(enumerate(get_building_names()))

    date_form = DateForm(request.POST or None)

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
        'time': timestamp,
        'date_form': date_form
    }
    return render(request, 'specific_building_monthly_users.html', tparams)

def line_graph(request, building = None):
    latestTS = get_last_ts()
    building = str(building)
    if(building != None):
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'"+building +"\' and time >=\'"+latestTS+"\'-24h GROUP BY time(15m)) group by time(1h)").raw['series'][0]["values"]
    print(values)
    labels = []
    data = []

    for sample in values:
        labels.append(sample[0][sample[0].find('T')+1: -4])
        data.append(sample[1])


    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def line_graph_monthly_users(request, building = None):
    latestTS = get_last_ts()   #vai buscar o último timestamp da base de dados
    if(building != None):
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'"+ building +"\' and time <\'"+latestTS+"\'-24h GROUP BY time(15m)) group by time(24h)").raw['series'][0]["values"]
    print(values)
    labels = []
    data = []

    for sample in values:
        labels.append(sample[0][sample[0].find('202')+5: -10])
        data.append(sample[1])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def users_per_month(request):
    return JsonResponse(data={
        'labels': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"],
        'data': [2020, 3050, 2500, 4050, 6230, 5022, 3035, 3210, 2080, 3090, 4020, 3272],
    })

def users_per_week(request):
    lst = []
    data = []
    for i in range(1, 54):
        lst.append(i)
        data.append(random.randint(1000))

    return JsonResponse(data={
        'labels': lst,
        'data': data
    })

def downloadChart(request):
    aps = []
    data = []
    for i in range(1,11):
        aps.append("AP-"+str(i))
        data.append(random.randint(5000))

    return JsonResponse(data={
      'labels': aps,
      'data': data
    })

def uploadChart(request):
    aps = []
    data = []
    for i in range(1, 11):
        aps.append("AP-" + str(i))
        data.append(random.randint(5000))

    return JsonResponse(data={
        'labels': aps,
        'data': data
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
    res = Departments.objects.all().order_by('name')
    print(res)
    buildings = []

    for x in res:
        buildings.append(str(x))

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

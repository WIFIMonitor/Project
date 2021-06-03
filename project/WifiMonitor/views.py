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

def get_timelapse_dictionary(dataset,starttime,measure):
    # query values between last measurement, minus 15 minutes
    sq = "select id,clientsCount from clientsCount where time >=\'"+starttime
    print(sq)
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

def heatmap(request):
    date_form = DateForm(request.POST or None)
    intent_form = IntentionForm(request.POST or None)
    graph = None

    if(request.method=='POST'):
        # Check whether timelapse or intent form were submitted
        if 'timelapse_submit' in request.POST:
            if date_form.is_valid():
                start = date_form.cleaned_data.get('start')
                end = date_form.cleaned_data.get('end')
                days = end-start

                #generate timelapse graph
                graph = generateTimelapse(start,days)

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
        'graph': graph
        }

    return render(request, 'heatmap.html', params)

def overview(request):
    latestTS = get_last_ts()
    labels, data1, data2 = population_building_graph()
    labelMonth, dataMonth = users_per_month()
    labelWeek, dataWeek = users_per_week()
    data2_4, data5 = frequencyUsage()
    download, upload = bandwidthUsage()

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
        'residentials_people_count': residentials_people_count,
        'campus_people_count': campus_people_count,
        'time': timestamp,
        'labels': labels,
        'data1': data1,
        'data2': data2,
        'labelMonth': labelMonth,
        'labelWeek': labelWeek,
        'dataMonth': dataMonth,
        'dataWeek': dataWeek,
        'data2_4': data2_4,
        'data5': data5,
        'download': download,
        'upload': upload,
    }
    return render(request, 'overview.html', tparams)

def campus_distribution(request):
    return render(request, 'campus_distribution.html')

def population_building_graph():
    count = get_buildings_count()
    labels = list(count.keys())
    data1 = list(count.values())

    data2 = []
    for i in range(1, 53):
        data2.append(random.randint(25))
    
    return labels,data1,data2

def specific_building(request, building=None):
    global prev_id
    specific_build_form = SpecificBuildingForm(request.POST or None)
    devices = []
    devicesData = []
    labelsMonth = []
    dataMonth = []
    dataDist=[]
    labelsDist=[]
    labelDownload = []
    labelUpload = []
    dataDownload = []
    dataUpload = []
    labelsWeek = []
    dataWeek = []

    if(request.method=='POST'):
        if specific_build_form.is_valid():
            building = specific_build_form.cleaned_data.get('departs')
            dataDist,labelsDist = line_graph(building)
            labelDownload,dataDownload = downloadChart()
            labelUpload,dataUpload = uploadChart()
            devices, devicesData = devicesTypes()
            labelsMonth, dataMonth = usersMonth()
            labelsWeek, dataWeek = usersWeek()

    prev_id = id
    tparams = {
        'buildings': "Building",
        'default_message': "Building",
        'time': timestamp,
        'specific_building_form': specific_build_form,
        'dataDist': dataDist,
        'labelsDist' : labelsDist,
        'labelDownload' : labelDownload,
        'dataDownload' : dataDownload,
        'labelUpload' : labelUpload,
        'dataUpload': dataUpload,
        'devices': devices,
        'dataDevices': devicesData,
        'labelsMonth': labelsMonth,
        'dataMonth': dataMonth,
        'labelsWeek': labelsWeek,
        'dataWeek': dataWeek
    }
    return render(request, 'specific_building.html', tparams)

def line_graph(building = None):
    latestTS = get_last_ts()
    building = str(building).lower()
    if(building != None):
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'"+building +"\' and time >=\'"+latestTS+"\'-24h GROUP BY time(15m)) group by time(1h)").raw['series'][0]["values"]
    labels = []
    data = []

    for sample in values:
        labels.append(sample[0][sample[0].find('T')+1: -4])
        data.append(sample[1])


    return data,labels

def users_per_month():
    labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October","November", "December"]
    data=[2020, 3050, 2500, 4050, 6230, 5022, 3035, 3210, 2080, 3090, 4020, 3272]

    return labels,data

def users_per_week():
    lst = []
    data = []
    for i in range(1, 54):
        lst.append(i)
        data.append(random.randint(1000))

    return lst,data

def downloadChart():
    aps = []
    data = []
    for i in range(1,11):
        aps.append("AP-"+str(i))
        data.append(random.randint(5000))

    return aps,data

def uploadChart():
    aps = []
    data = []
    for i in range(1, 11):
        aps.append("AP-" + str(i))
        data.append(random.randint(5000))

    return aps,data

def frequencyUsage():
    buildings = get_building_names()
    data2_4 = []
    data5 = []

    for i in range(0, len(buildings)):
        data2_4.append(random.randint(500))
        data5.append(random.randint(500))

    return data2_4, data5

def bandwidthUsage():
    buildings = get_building_names()
    download = []
    upload = []

    for i in range(0, len(buildings)):
        download.append(random.randint(1000))
        upload.append(random.randint(1000))

    return download, upload

def devicesTypes():
    labels = ["Android", "IOS", "PC"]
    data = []

    for i in range(0, 3):
        data.append(random.randint(500))

    return labels, data

def usersMonth():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    data = []

    for i in range(0, len(labels)):
        data.append(random.randint(500))

    return labels, data

def usersWeek():
    lst = []
    data = []
    for i in range(1, 54):
        lst.append(i)
        data.append(random.randint(500))

    return lst, data

def get_buildings_count():
    latestTS = get_last_ts()
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount\" from clientsCount where time >= \'"+latestTS+"\'-15m ").raw['series'][0]["values"]
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
    buildings = []

    for x in res:
        buildings.append(str(x).lower())

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

def generateTimelapse(start,days):
    dataset = []
    start_time = datetime.strptime(str(start), "%Y-%m-%d").isoformat('T') + 'Z'

    # Generate timelaspes X timelapses, where X is 94 * days, because, theres 94 measures in each day
    for x in range(0,(94*days.days)):
        try:
            # since we get values every 15 minutes, we need to now how many 15 minute measures we want
            offset = str(15*x)
            offset2 = str(15*(x+1))
            query_time = start_time + "\' +"+offset+"m and time <= \'" + start_time + "\' + "+offset2+"m"

            get_timelapse_dictionary(dataset,query_time,x)
        except Exception as e:
            print(e)
            continue

    fig = px.density_mapbox(dataset, lat='lat', lon='lon', z='people', radius=10,animation_frame='measure',
            center=dict(lat=40.63193066543083, lon=-8.658186691344712),
            zoom=15,
            mapbox_style="stamen-terrain",
            width=500,
            height=700,
            color_continuous_scale= [
                    [0.0, "green"],
                    [0.3, "green"],
                    [0.5, "yellow"],
                    [0.7, "yellow"],
                    [0.9, "red"],
                    [1.0, "red"]],
            title= "Timelapse de: " + start_time[0:10] + " com 15 minutos de intervalo ",
            range_color=(0,30), #max and min values for heatmap
            )

    return fig.to_html(auto_play=False,full_html=False,include_plotlyjs=False,validate=False)

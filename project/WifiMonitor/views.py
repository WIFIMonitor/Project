from django.shortcuts import render
from influxdb import InfluxDBClient
import plotly.express as px
import json
from datetime import datetime, time, timedelta
from .forms import DateForm,IntentionForm,SpecificBuildingForm
from .models import Departments
from django.db.models import F,Sum
from numpy import random, signbit
import timeit
import time

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

def get_timelapse_dictionary(starttime,measure):
    # query values between last measurement, minus 15 minutes
    sq = "select id,clientsCount from clientsCount where time >=\'"+starttime
    # get the last 15m values, from the last value in DB, and not from now(), because CISCO PRIME can stop sending values
    try:
        people_count = client.query(sq).raw['series'][0]["values"]
    except:
        return []
    
    # create dataset of the measures between the two start and end times
    dataset = []
    for line in people_count:
        # only add to the timelapse points that have people conected, to not overload the array
        if line[2] != 0:
            if line[1] in coords:
                dic = { "lat": coords[line[1]]["lat"],
                        "lon":coords[line[1]]["lon"],
                        "people":line[2],
                        "measure":measure,
                        }
                dataset.append(dic)
            else:
                continue

    return dataset

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
                
                start_time = timeit.default_timer()
                #generate timelapse graph
                if days.days > 0:
                    graph = generateTimelapse(start,days)
                end_time = timeit.default_timer()
                print("Time taken to create timelapse: ", end_time-start_time)

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
    #next 3 lines evaluate the power of the database, if it is quick enough to respond it will call the weekly and monthly querry (high computacional power)
    start_time = time.time()
    client.query("select * from clientsCount where time >=\'"+get_last_ts()+"\'-15m")
    timetaken = time.time() - start_time
    latestTS = get_last_ts()
    labels, data1 = population_building_graph()
    labelMonth, dataMonth = users_per_month(timetaken)
    labelWeek, dataWeek = users_per_week(timetaken)
    data2_4, data5 = frequencyUsage()
    download, upload = bandwidthUsage(labels)

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
    
    return labels,data1

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
            devices, devicesData = devicesTypes(str(building).lower())
            labelsMonth, dataMonth = usersMonth(str(building).lower())
            labelsWeek, dataWeek = usersWeek(str(building).lower())

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

def users_per_month(timetaken):
    labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October","November", "December"]
    values = []
    if timetaken>1:
        values = []
    else:
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where time >=\'2021-05-03T22:28:44.139117Z\' GROUP BY time(15m)) group by time(720h)").raw['series'][0]["values"]
    data=[]
    j=0
    for i in range(1, 12):
        if i<5:
            data.append(0)
        elif j<len(values):
            data.append(float("{:.2f}".format(values[j][1])))
            j+=1
        else:
            data.append(0)

    return labels,data

def users_per_week(timetaken):
    lst = []
    values = []
    if timetaken>1:
        values = []
    else:
        values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where time >=\'2021-05-03T22:28:44.139117Z\' GROUP BY time(15m)) group by time(168h)").raw['series'][0]["values"]
    data = []
    j=0
    for i in range(1, 54):
        lst.append(i)
        if i<20:
            data.append(0)
        elif j<len(values):
            data.append(float("{:.2f}".format(values[j][1])))
            j+=1
        else:
            data.append(0)

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
    count2_4 = get_building_24_ghz()
    count5 = get_building_5_ghz()
    
    data2_4 = list(count2_4.values())
    data5 = list(count5.values())

    return data2_4, data5

def bandwidthUsage(labels):
    values=[]
    try:
        values = client.query("select * from metricsBuildingCount where time>now()-1h").raw['series'][0]["values"]
    except:
        print("ERROR: no recent information about bandwith usage")
    
    buildings = labels
    download = []
    upload = []
    ls_name = []
    ls = [] 

    for i in reversed(values):
        if not i[1] in ls_name:
            ls.append(i)
            ls_name.append(i[1])

    for i in buildings:
        for j in range(1, len(ls)):
            if ls[j][1].lower() == i:
                download.append(ls[j][3])
                upload.append(ls[j][2])
                break
            elif j==len(ls)-1:
                download.append(0)
                upload.append(0)

    return download, upload

def devicesTypes(building):
    latestTS = get_last_ts()
    labels = ["Android", "IOS", "PC"]
    values=[]
    try:
        values = client.query("select \"ap_name\",\"android\",\"ios\",\"laptop\" from devicesTypes where time >= \'"+latestTS+"\'-1h and \"building\" = \'" + building + "\'").raw['series'][0]["values"]
    except:
        print("ERROR: building doesn't provide information about devices types")

    ls = []
    android = 0
    ios=0
    laptop=0
    for i in reversed(values):
        if not i[1] in ls:
            ls.append(i[1])
            android+=i[2]
            ios+=i[3]
            laptop+=i[4]
        
    data = [android, ios, laptop]

    return labels, data

def usersMonth(building):
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    data = []

    latestTS = get_last_ts()
    values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'" + building + "\' and time >=\'2021-05-07T00:46:37.506123Z\'-1h GROUP BY time(15m)) group by time(720h)").raw['series'][0]["values"]

    j=0
    for i in range(0, len(labels)):
        if i<4:
            data.append(0)
        elif j<len(values):
            data.append(values[j][1])
            j+=1
        else:
            data.append(0)
    return labels, data

def usersWeek(building):
    lst = []
    data = []
    values = client.query("select mean(\"sum\")from (select sum(\"clientsCount\") from clientsCount where \"building\" = \'" + building + "\' and time >=\'2021-05-07T00:46:37.506123Z\'-1h GROUP BY time(15m)) group by time(168h)").raw['series'][0]["values"]
    j=0
    for i in range(1, 54):
        lst.append(i)
        if i<19:
            data.append(0)
        elif j<len(values):
            data.append(values[j][1])
            j+=1
        else:
            data.append(0)
        
    return lst,data

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

def get_building_24_ghz():
    latestTS = get_last_ts()
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount2_4Ghz\" from clientsCount where time >= \'"+latestTS+"\'-15m ").raw['series'][0]["values"]
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

def get_building_5_ghz():
    latestTS = get_last_ts()
    try:
        #query para obter os n de pessoas conectados a cada ap no intervalo entre[0-15min]. o +45min da query deve-se ao facto do now() devolver em utc
        res = client.query("select \"building\",\"clientsCount5Ghz\" from clientsCount where time >= \'"+latestTS+"\'-15m ").raw['series'][0]["values"]
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
    #create a dataset with the measures for the day
    dataset = []
    start_time = datetime.strptime(str(start), "%Y-%m-%d").isoformat('T')
    # add hours,minutes and seconds precision to above date
    time_measure= datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S') 
    # Generate timelaspes X timelapses, where X is 96 * days, because, theres 96 measures in each day
    for x in range(0,(96*days.days)):
        try:
            # since we get values every 15 minutes, we need to now how many 15 minute measures we want
            offset = str(15*x)
            offset2 = str(15*(x+1))
            query_time = start_time + "Z\' +"+offset+"m and time <= \'" + start_time + "Z\' + "+offset2+"m"
            # add 15 minutes to each query, for better visualization of the slider
            measure_time = time_measure + timedelta(minutes=(float(offset2)))
            slider_step = str(measure_time)[11:16] # only get the Hours:Minutes part of the string
            # extend yeilds better performance, rather than apppending an array of 776 items
            dataset.extend(get_timelapse_dictionary(query_time,slider_step))
        except Exception as e:
            print(e)
            continue
    # create the timelapse, where the slider represents the time of the measure of people connected
    fig = px.density_mapbox(dataset, lat='lat', lon='lon', z='people', radius=10,animation_frame='measure',
            center=dict(lat=40.63193066543083, lon=-8.658186691344712),
            zoom=15,
            mapbox_style="stamen-terrain",
            width=900,
            height=700,
            color_continuous_scale= [   # color scale for the heatmap
                    [0.0, "green"],
                    [0.3, "green"],
                    [0.5, "yellow"],
                    [0.7, "yellow"],
                    [0.9, "red"],
                    [1.0, "red"]],
            title= "Timelapse de: " + start_time[0:10], 
            range_color=(0,30), #max and min values for heatmap
            )
    return fig.to_html(auto_play=False,full_html=False,include_plotlyjs=False,validate=True)

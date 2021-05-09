from django.http import JsonResponse
from django.shortcuts import render


def index(request):

    return render(request,'index.html')


def map(request):
    return render(request,'map.html')


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

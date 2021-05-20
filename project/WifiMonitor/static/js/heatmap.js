// This example requires the Visualization library. Include the libraries=visualization
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=visualization">
var dados = [];
let markersArray = [];
function loadMap() {

    for (var i = 0; i < heatmapData.length; i++) {
        dados.push({location: new google.maps.LatLng(heatmapData[i].lat, heatmapData[i].lon), weight: heatmapData[i].people});
    }

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 16,
        center: {lat: 40.63129560, lng: -8.65810583},
        mapTypeId: "satellite",
    });

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: dados,
        map: map,
        maxIntensity: 70,
        radius: 25,
        opacity: 0.6
    });

    map.addListener('zoom_changed', () => {
        zoom = map.getZoom();
        var radius = 3.076+0.00294182*Math.pow(2.71828, 0.561249*(zoom));
        var maxintensity = 48.9302+0.0475174*Math.pow(2.71828, 0.244225*(zoom));
        if (radius < 0) radius = 10;
        heatmap.set("radius", radius);
        heatmap.set("maxIntensity", maxintensity);
    });
    
    // criar a janela de informação que é ativada quando se clica num AP
    const infowindow = new google.maps.InfoWindow({});
    
    for (var i = 0; i < heatmapData.length; i++) {
        //criar um marker nas coordenadas do AP
        const marker = new google.maps.Marker({
            position: new google.maps.LatLng(heatmapData[i].lat, heatmapData[i].lon),
            icon: {
                url: 'https://png.vector.me/files/images/3/8/387560/wireless_logo_preview',
                scaledSize: new google.maps.Size(30, 30)
            },
            title: "Latitude: " + heatmapData[i].lat + " Longitude: " + heatmapData[i].lon + " Pessoas: " + heatmapData[i].people,
            map: map,
        });
        // colocar o marker escondido por defeito
        marker.category = 1;
        marker.setVisible(false);
        
        // adicionar um listener, para quando se clica nele, aparecer uma janela de informação
        marker.addListener('click', () => {
            infowindow.close();
            infowindow.setContent(marker.getTitle());
            infowindow.open(map, marker);
        });

        //adicionar o marker ao array de markers, para conseguir-mos dar toggle ON e OFF
        markersArray.push(marker);
    }
    


}

function displayMarkers(obj, category) {
    var i;
    for (i = 0; i < markersArray.length; i++) {
        if (markersArray[i].category === category) {
            if ($(obj).is(":checked")) {
                markersArray[i].setVisible(true);
            } else {
                markersArray[i].setVisible(false);
            }
        }
        else {
            markersArray[i].setVisible(false);
        }
    }
}

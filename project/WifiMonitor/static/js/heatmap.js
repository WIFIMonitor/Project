var dados = [];
let markersArray = [];
let map;
let displayFlag = true;
function loadMap() {

    // criar a janela de informação que é ativada quando se clica num AP
    const infowindow = new google.maps.InfoWindow({});

    // create the map
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 16,
        center: {lat: 40.63129560, lng: -8.65810583},
        mapTypeId: "satellite",
    });

    for (var i = 0; i < heatmapData.length; i++) {
        // only add to the heatmap, AP's that have people connected. They still get added to the markers with 0 people connected
        if(heatmapData[i].people > 0){
            dados.push({location: new google.maps.LatLng(heatmapData[i].lat, heatmapData[i].lon), weight: heatmapData[i].people});
        }
        
        //criar um marker nas coordenadas do AP
        const marker = new google.maps.Marker({
            position: new google.maps.LatLng(heatmapData[i].lat, heatmapData[i].lon),
            icon: {
                url: '/static/images/ap_icon.ico',
                scaledSize: new google.maps.Size(20, 20)
            },
            title: "Latitude: " + heatmapData[i].lat + " | Longitude: " + heatmapData[i].lon + " | Pessoas: " + heatmapData[i].people + " | Piso: "+heatmapData[i].piso,
            map: map,
        });
        // colocar o marker escondido por defeito
        marker.setVisible(false);

        // adicionar um listener, para quando se clica nele, aparecer uma janela de informação
        marker.addListener('click', () => {
            infowindow.close();
            infowindow.setContent(marker.getTitle());
            infowindow.open(map, marker);
        });

        // adicionar um listener ao marker, para quando o rato sai do icon, a janela de informação desaparecer
        marker.addListener('mouseout', () => {
            infowindow.close();
        })

        //adicionar o marker ao array de markers, para conseguir-mos dar toggle ON e OFF
        markersArray.push(marker);
    }


    const centerApShow = document.createElement("div");
    CenterControl(centerApShow, map);
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerApShow);

    // criar a layer do heatmap
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: dados,
        map: map,
        maxIntensity: 70,
        radius: 25,
        opacity: 0.6
    });
    
    // adicionar um Listener ao Mapa, para ajustar os valores de raio e maxIntensity quando o zoom muda
    map.addListener('zoom_changed', () => {
        zoom = map.getZoom();
        var radius = 3.076 + 0.00294182 * Math.pow(2.71828, 0.561249 * (zoom));
        var maxintensity = 48.9302 + 0.0475174 * Math.pow(2.71828, 0.244225 * (zoom));
        if (radius < 0) radius = 10;
        heatmap.set("radius", radius);
        heatmap.set("maxIntensity", maxintensity);
    });
}

// Sets the map on all markers in the array.
function setVisibility(visibility) {
    for (j = 0; j < markersArray.length; j++) {
        markersArray[j].setVisible(visibility);
    }
}

function displayMarkers() {
    // show
    if (displayFlag) {
        setVisibility(displayFlag);
    } else {
        //hide
        setVisibility(displayFlag);
    }
    displayFlag = !displayFlag;
}

function CenterControl(controlDiv) {
    // Set CSS for the control border.
    const controlUI = document.createElement("div");
    controlUI.style.backgroundColor = "#fff";
    controlUI.style.border = "2px solid #fff";
    controlUI.style.borderRadius = "3px";
    controlUI.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
    controlUI.style.cursor = "pointer";
    controlUI.style.marginTop = "8px";
    controlUI.style.marginBottom = "22px";
    controlUI.style.textAlign = "center";
    controlUI.title = "Click to show AP's";
    controlDiv.appendChild(controlUI);
    // Set CSS for the control interior.
    const controlText = document.createElement("div");
    controlText.style.color = "rgb(25,25,25)";
    controlText.style.fontFamily = "Roboto,Arial,sans-serif";
    controlText.style.fontSize = "16px";
    controlText.style.lineHeight = "38px";
    controlText.style.paddingLeft = "5px";
    controlText.style.paddingRight = "5px";
    controlText.innerHTML = "Show All AP's";
    controlUI.appendChild(controlText);
    // Setup the click event listeners: simply set the map to Chicago.
    controlUI.addEventListener("click", () => {
        displayMarkers();
    });
}

// Function to create image based on the google maps heatmap
function timelapse() {
    html2canvas(document.querySelector("#map"), {
        useCORS: true,
        scale: 0.5,
    }).then(canvas => {
        var image = canvas.toDataURL("image/jpeg",0.5).replace("image/jpeg", "image/octet-stream");
        window.location.href = image;
    });
}

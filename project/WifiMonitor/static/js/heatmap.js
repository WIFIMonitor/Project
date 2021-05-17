// This example requires the Visualization library. Include the libraries=visualization
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=visualization">
let map, heatmap;

function myMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 17,
    center: { lat: 40.63129560, lng: -8.65810583 },
    mapTypeId: "satellite",
  });
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: getData(),
    map: map,
    radius: 25,
    });
}

function getData(){
	
	var heatmapData = "{{data|safe}}";
    console.log(heatmapData);

	//for(var j=0;j<locations.length;j++)
	//{
	//	heatmapData.push(new google.maps.LatLng(locations[j].Latitude,locations[j].Longitude));
	//}

	return heatmapData;
}

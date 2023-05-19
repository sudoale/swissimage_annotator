let map;

function initMap() {
    map = L.map('map').setView([46.8, 8], 8);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 16,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const downloadButton = document.getElementById("downloadLeaflet");

    downloadButton.addEventListener("click", () => {

    const project_select = document.getElementById("projectDropdownLeaflet");
    let request_data = {};
    let bounds = map.getBounds();

    if (project_select.value !== 'default') {
      request_data.project_name = project_select.value;
      request_data.map_type = 'leaflet';
      request_data.north = bounds._northEast.lat;
      request_data.east = bounds._northEast.lng;
      request_data.south = bounds._southWest.lat;
      request_data.west = bounds._southWest.lng;

      console.log(JSON.stringify(request_data));

      let request = $.ajax({
        url: "/download",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(request_data)
      });
      request.done(function (response, textStatus, jqXHR) {
        if (!response["success"]) {
          alert(response["message"]);
          map.setZoom(14);
        } else {
          console.log("it worked");
          window.open('/' +  project_select.value + '/annotate', '_self');
        }
      });
    }
    else{
      alert("Please create/select a project first.")
    }
  })
}


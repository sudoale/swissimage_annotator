let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 46.8, lng: 8 },
    zoom: 8,
  });

  const input = document.getElementById("pac-input");
  const dropDown = document.getElementById("dropdown");
  const downloadButton = document.getElementById("download");
  const searchBox = new google.maps.places.SearchBox(input);

  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(dropDown);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(downloadButton);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  let markers = [];

  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          map,
          icon,
          title: place.name,
          position: place.geometry.location,
        })
      );
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });

  downloadButton.addEventListener("click", () => {
    console.log(map.getZoom());
    const project_select = document.getElementById("dropdown");
    let request_data = map.getBounds(true);
    if (project_select.value !== 'default') {
      request_data.project = project_select.value;
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
        }
      });
    }
    else{
      alert("Please create/select a project first.")
    }
  });
}


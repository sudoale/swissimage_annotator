
function download(x, y){
    const project_select = document.getElementById("projectDropdown");

    if (project_select.value !== 'default') {
        request_data = {"x": x, "y": y, "project_name":  project_select.value,
        "map_type": "swisstopo"};
        request = $.ajax({
          url: "/download",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(request_data)
        });
        request.done(function (response, textStatus, jqXHR){
            window.open('/' + project_select.value + '/annotate', '_self');
        });
    }
    else{
      alert("Please create/select a project first.")
    }
}
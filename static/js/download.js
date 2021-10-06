function download(x, y, project){
        request_data = {"x": x, "y": y, "project": project};
        request = $.ajax({
          url: "/download",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(request_data)
        });
        request.done(function (response, textStatus, jqXHR){
            window.open('/annotate', '_self');
        });
}
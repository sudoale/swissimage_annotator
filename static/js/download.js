function download(x, y, project){
        request_data = {"x": x, "y": y, "project_name": project};
        request = $.ajax({
          url: "/download",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(request_data)
        });
        request.done(function (response, textStatus, jqXHR){
            window.open('/' + project + '/annotate', '_self');
        });
}
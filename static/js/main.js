$(document).ready(function(){
    $("img").click(function(){
      $(this).toggleClass("selected");
    });
});

const projectNameHolder = document.getElementById("projectName");

function annotateImages(){
    result = [];

    $("img").each(function(){
        var img_state = {'src': $(this).attr('src'),
                         'selected': $(this).attr("class").includes('selected')};
        result.push(img_state);
    });
    sendImageData = $.ajax({
          url: "/" + projectNameHolder.textContent + "/annotate",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(result),
          success: function(data){
            $.get({
                  url: "/" + projectNameHolder.textContent + "/annotate/next",
                  success: function(data){
                    console.log(data);
                    if(!data.images){
                        window.open('/view/2758000/1191000', '_self');
                      }
                    $("img").each(function(i, element){
                        $(this).attr('src', data.images[i])
                        console.log(data.images[i]);
                    });
                  }
            });
          }
    });
    $(".selected").each(function(){
      $(this).toggleClass("selected");
    });
}




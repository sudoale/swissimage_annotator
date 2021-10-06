$(document).ready(function(){
    $("img").click(function(){
      $(this).toggleClass("selected");
    });
});

function annotateImages(){
    result = [];
    $("img").each(function(){
        var img_state = {'src': $(this).attr('src'),
                         'selected': $(this).attr("class").includes('selected')};
        result.push(img_state);
    });
    sendImageData = $.ajax({
          url: "/annotate",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(result),
          success: function(data){
            $.get({
                  url: "/annotate/next",
                  success: function(data){
                    console.log(data);
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




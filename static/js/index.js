const createProjectButton = document.getElementById("createProject");
const projectNameInput = document.getElementById("projectName");

createProjectButton.addEventListener("click", () => {
    postData = {"project_name": projectNameInput.value};

    console.log(postData);

    sendImageData = $.ajax({
          url: "/create_project",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(postData),
          success: function(data){
              console.log(data);
          }
    });
});
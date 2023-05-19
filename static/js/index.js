const createProjectButton = document.getElementById("createProject");
const projectNameInput = document.getElementById("projectName");

createProjectButton.addEventListener("click", () => {
    let postData = {"project_name": projectNameInput.value};

    console.log(postData);

    let createProjectRequest = $.ajax({
          url: "/create_project",
          type: "post",
          contentType: "application/json",
          data: JSON.stringify(postData)
    });
    createProjectRequest.done(function (response, textStatus, jqXHR){
        if (!response["success"]) {
          alert('Project not created, please try again!');
        } else {
            alert('Project created successfully!');
            window.open('/view/2758000/1191000', '_self');
        }
    })
});
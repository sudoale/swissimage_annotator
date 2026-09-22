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

document.querySelectorAll('.crop-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const project = this.dataset.project;
        const statusSpan = document.getElementById('status-' + project);
        statusSpan.textContent = 'Cropping...';
        fetch('/crop_project/' + project, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusSpan.textContent = '✅ ' + data.message;
            } else {
                statusSpan.textContent = '❌ Error: ' + data.message;
            }
        })
        .catch(err => {
            statusSpan.textContent = '❌ Request failed.';
        });
    });
});
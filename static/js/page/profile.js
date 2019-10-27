let repo_json = "";

function init() {
    getRepo()
}

function getRepo() {
    request = new XMLHttpRequest();
    request.open("GET", "/api/repos");
    request.onreadystatechange = function () {
        if(request.status === 200)
        {
            repo_json = request.responseText;
        }
    };
    request.send();

}



let repo_json;
let repo_json_str;

function init() {
    getRepo()
}

function getRepo() {
    let request = new XMLHttpRequest();
    request.open("GET", "/api/repos");
    request.onreadystatechange = function () {
        if (!(request.readyState === 4 && request.status === 200)) return;
        if (request.status === 200) {
            repo_json_str = request.responseText;
            render(repo_json_str)
        }
    };
    request.send();

}

/*

<div class="repo-card w-100">
    <h4>타이틀</h4>
    <h5>만든날</h5>
    <h6>pull request</h6>
    <h6>commit</h6>
    <h6>fork</h6>
    <h6>License</h6>
</div>

 */
let app = new Vue({
      el: '#rc',
      data: {
        repos: []
      },
      delimiters: ['[[',']]']
});
function render(json_data) {
    repo_json = JSON.parse(json_data.toString());

    document.getElementById("rc").style.display = "flex";

    app.repos = repo_json;
    app.forceUpdate();


}

/*
 * visibility: all, public, private
 * affiliation: owner,collaborator,organization_member
 * type: all, owner, public, private, member
 * sort: created, updated, pushed, full_name
 * direction: asc, desc
 */
function setFilter(visibility)
{

}



function prof_refresh() {
    let request = new XMLHttpRequest();
    request.open("GET", "/api/repos/refresh");
    request.onreadystatechange = function () {
        if (!(request.readyState === 4 && request.status === 200)) return;
        if (request.status === 200) {
            repo_json_str = request.responseText;
            getRepo();
        }
    };
    request.send();
}

let repo_json;
let repo_json_str;

function init() {
    getRepo()
}

function getRepo() {
    request = new XMLHttpRequest();
    request.open("GET", "/api/repos");
    request.onreadystatechange = function () {
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

function render(json_data) {

    repo_json = JSON.parse(json_data);


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
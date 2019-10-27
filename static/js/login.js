function checkLogin() {
    const requester = new XMLHttpRequest();
    requester.open("GET", "/auth/status");
    requester.onreadystatechange = function () {
        let state = requester.responseText === "yes";
        loginElementReload(state)
    };
    requester.send();
}

function loginElementReload(login) {
    if(login)
        isLogin();
    else
        isLogout();
}

function isLogin() {
    document.getElementById("logout-button").style.display = "block";
    document.getElementById("login-button").style.display = "none";
}

function isLogout() {
    document.getElementById("logout-button").style.display = "none";
    document.getElementById("login-button").style.display = "block";
}

function loginHandler() {
    window.open("/auth/login", "login", "width=500, height=600")
    //window.open("/auth/login");
    //location.href = "/auth/login";
}

function logoutHandler() {
    location.href = "/auth/logout"
    /*
    const requester = new XMLHttpRequest();
    requester.open("POST", "/auth/logout");
    requester.send();
    requester.onreadystatechange = function() { checkLogin() }*/
}
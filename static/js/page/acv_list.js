let acv_card = new Vue(
    {
        el:"#alc",
        data:
            {
                acvs:[
                    {img:"", title:"", ainfo:"", aid:-1}
                ]

            },
        delimiters: ['[[',']]']
    }
);

function acv_list() {
    let requester = new XMLHttpRequest();
    requester.open("GET", "/api/achv");
    requester.onreadystatechange = function () {
        if (!(requester.readyState === 4 && requester.status === 200)) return;
        let r = JSON.parse(requester.responseText)
        r.sort(function (a, b) {
            return a.aid - b.aid;
        });
        acv_card.acvs = r;
    };
    requester.send()
}
let achv_cards = new Vue(
    {
        el:"#glc",
        data:
            {
                galls:[
                    {img:"", title:"", info:"", gid:-1}
                ]

            },
        delimiters: ['[[',']]']
    }
);

function gall_list() {
    let requester = new XMLHttpRequest();
    requester.open("GET", "/api/achvs");
    requester.onreadystatechange = function () {
        achv_card.achvs = JSON.parse(requester.responseText)
    };
    requester.send()
}
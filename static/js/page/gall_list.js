let gall_cards = new Vue(
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
    requester.open("GET", "/api/gallery");
    requester.onreadystatechange = function () {
        gall_cards.galls = JSON.parse(requester.responseText)
    };
    requester.send()
}
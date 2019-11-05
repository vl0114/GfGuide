let acvRender = new Vue({
        el: '#acv',
        data: {
            contents: '<h1>로딩중</h1>'
        },
    delimiters: ['[[',']]']
});

function acv_init()
{
    let url = "/api/achv/".concat(aid);
    let req = new XMLHttpRequest();
    req.open('GET', url);
    req.onreadystatechange = function () {
        if (!(req.readyState === 4 && req.status === 200)) return;
        let j = JSON.parse(req.responseText);
        acvRender.contents = j.contents;
    };
    req.send();
}

function checkThis() {
    let url = "/api/achv/check/".concat(aid);
    let req = new XMLHttpRequest();
    req.open('GET', url);
    req.onreadystatechange = function () {
        if (req.readyState === 4 && req.status === 200) {
            let r = req.responseText;
            console.log(r);
            if (r === 'YES')
                isYes();
            else
                isNo();
        }
    };
    req.send();
}

function isYes() {
    alert('정답입니다.');
}

function isNo() {
    alert('오답입니다.')
}
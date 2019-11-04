from flask import Flask, redirect, request, session, render_template, url_for, abort
from src import GitHubLogin, GithubUser, caching, gh_db
import randstr
from src import gh_init, Setting

app = Flask(__name__)
app.secret_key = 'dsadadsadasdadadsa'  # randstr.randstr(40)


#### page ####
## 제공 페이지


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    session['rand_key'] = randstr.randstr(40)
    return render_template('index.html')


@app.route('/profile')
def profile():
    if 'gh_token' not in session:
        abort(403)
    api = caching.Caching.get(session['user_manager'])
    return render_template('page/profile.html',
                           img_src=api.prof_img(),
                           user_name=api.user_name(),
                           user_site=api.user_site())


@app.route('/achievement')
def achievement():
    return '<body><script>alert("서비스 준비중 입니다"); window.location.href = "/";</script></body>'


@app.route('/license')
def redirect_license():
    return redirect('https://github.com/vl0114/GhGuide')


@app.route('/study')
def study():
    if 'login_key' not in session or session['login_key'] is None:
        abort(403)  # redirect error page
    return render_template('page/gall_list.html')


@app.route('/study/<g>')
def study_page(g: str):
    if 'login_key' not in session or session['login_key'] is None:
        abort(403)  # redirect error page
    gdb = GithubUser.Gallery()
    if g.isdecimal():
        if not gdb.is_in(int(g)):
            abort(404)
        return render_template('page/study.html', gid=int(g))
    else:
        if not gdb.is_in(g):
            abort(404)
        return render_template('page/study.html', gid=gdb.search_dict(g)['gid'])


@app.route('/bbooiiww/doggos')
def egg():
    return """
    <iframe width="1252" height="704"
     src="https://www.youtube.com/embed/5rJih7rWXMA"
     frameborder="0" allow="accelerometer;
     autoplay; encrypted-media; gyroscope; picture-in-picture"
     allowfullscreen></iframe>
    """


@app.route('/bbooiiww/weeeeed')
def my_mental_state():
    return """
    <iframe width="1004" height="753"
     src="https://www.youtube.com/embed/oF9yHO-UUws"
      frameborder="0" allow="accelerometer; autoplay;
       encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe>
    """


@app.route('/editor')
def editor_page():
    if 'login_key' not in session or session['login_key'] is None:
        abort(403)  # redirect error page
    if session['uid'] not in Setting.Admin.admin_uid:
        abort(403)
    return render_template('page/editor.html')


#### error page ####
## 에러 페이지
@app.errorhandler(404)
def err_404(error):
    return render_template('page/error/4XX/404.html')


@app.errorhandler(403)
def err_403(error):
    return render_template('page/error/4XX/403.html')


@app.errorhandler(408)
def err_408(error):
    return render_template('page/error/4XX/408.html')


@app.errorhandler(400)
def err_400(error):
    return render_template('page/error/4XX/400.html')


@app.errorhandler(500)
def err_500(error):
    return render_template('page/error/5XX/500.html')


@app.errorhandler(502)
def err_502(error):
    return render_template('page/error/5XX/502.html')


@app.errorhandler(503)
def err_503(error):
    return render_template('page/error/5XX/503.html')


@app.errorhandler(504)
def err_504(error):
    return render_template('page/error/5XX/504.html')


#### login ####
## 로그인 담담
## 로그인시 세션과 콜백시 세션이 다르면 에러


## 로그인
@app.route('/auth/login')
def login():
    if 'gh_token' in session and session['gh_token'] is not None:
        return redirect('/auth/login_success')
    l_key = randstr.randstr(40)
    session['login_key'] = l_key
    url = GitHubLogin.GHLogin.generate_gh_redirect_url(l_key)
    return redirect(url)


## 요청 콜백 핸들러
@app.route('/auth/cb')
def callback():
    session['temp'] = 4
    code = request.args.get('code')
    l_key = request.args.get('state')
    if code is None or l_key is None:
        abort(400)  # redirect error page

    if 'login_key' not in session:
        abort(403)  # redirect error page

    if session['login_key'] != l_key:
        abort(403)

    token = GitHubLogin.GHLogin.request_token(code)
    session['gh_token'] = token
    return redirect('/auth/login_success')


## 부모창 새로고침, 현재창 닫기, 필요한 함수 요청
@app.route('/auth/login_success')
def login_success():
    if 'gh_token' not in session:
        abort(403)
    if 'user_manager' in session:
        caching.Caching.rm(session['user_manager'])
    if 'repo_manager' in session:
        caching.Caching.rm(session['repo_manager'])

    chk = session['login_key'] + 'user'
    caching.Caching.save(chk, GithubUser.GitHubUser(session['gh_token']))
    session['user_manager'] = chk
    caching.Caching.get(session['user_manager']).user_login()
    caching.Caching.get(session['user_manager']).refresh_user_data()
    session['uid'] = caching.Caching.get(session['user_manager']).get_uid()
    chk = session['login_key'] + 'repo'
    caching.Caching.save(chk, GithubUser.GitHubRepo(session['gh_token'], session['uid']))
    session['repo_manager'] = chk
    return '<html?<head></head><body><script>opener.location.reload();close();</script></body></html>'


## 로그인 상태
@app.route('/auth/status')
def login_status():
    if 'gh_token' in session and session['gh_token'] is not None:
        return 'yes'
    else:
        return 'no'


## 로그아웃
@app.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    if 'gh_token' not in session:
        abort(403)
    caching.Caching.rm(session['user_manager'])
    caching.Caching.rm(session['user_manager'])
    if request.method == 'POST':
        if 'gh_token' not in session:
            return 'logouted'
        session.pop('gh_token')
        return 'OK'
    else:
        if 'gh_token' not in session:
            return 'logouted'
        session.pop('gh_token')
        return redirect('/')


#### api ####
## 클라이언트에서 사용할 api


@app.route('/session_clear')
def session_clear():
    session.clear()
    return redirect("/")


@app.route('/api/repos')
def repos():
    if 'gh_token' not in session:
        return '', 403

    return caching.Caching.get(session['repo_manager']).get_repos_json()


@app.route('/api/repos/refresh')
def repo_refresh():
    caching.Caching.get(session['repo_manager']).refresh_repos()
    return 'OK'


@app.route('/api/gallery')
@app.route('/api/gallery/list')
def gall_list():
    gall = GithubUser.Gallery()
    return gall.get_list()


@app.route('/api/gallery/<gid>')
def gall_post_list(gid: int):
    gall = GithubUser.Gallery()
    gall.set(gid)
    return gall.post_list()


@app.route('/api/post/<pid>')
def get_post(pid: int):
    try:
        post = GithubUser.Post()
        post.set(pid)
        return post.get_post()
    except:
        return '', 404


# ? title, content
#   create post in gallery<gid>
@app.route('/api/post/add/<gid>', methods=['GET', 'POST'])
def add_post(gid: int):
    if request.method == 'POST':
        writer = gh_db.post()
        writer.new(gid, request.form['title'], request.form['content'], 'html', session['uid'])
        return 'OK'
    if request.method == 'GET':
        writer = gh_db.post()
        writer.new(gid, request.args['title'], request.args['content'], 'html', session['uid'])
        return 'OK'
    return 'NO', 503


# ? title, info
#   create gallery
@app.route('/api/gallery/add', methods=['GET', 'POST'])
def add_gall():
    try:
        gall = GithubUser.Gallery()
        gall.create(request.args['title'], request.args['info'])
        return 'OK'
    except:
        return 'error', 403


# ? id=int
#   delete gallery with id param-id
@app.route('/api/gallery/rm', methods=['GET', 'POST'])
def del_gall():
    try:
        gall = GithubUser.Gallery()
        gall.search_id(int(request.args['id']))
        gall.rm()
        return 'OK'
    except:
        return 'error', 403


if __name__ == '__main__':
    gh_init.gh_init()
    app.run(host='0.0.0.0', port=80)

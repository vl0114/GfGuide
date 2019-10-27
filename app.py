from flask import Flask, redirect, request, session, render_template, url_for, abort
from src import GitHubLogin, GithubUser
import randstr

app = Flask(__name__)
app.secret_key = 'dsadadsadasdadadsa'


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
    api = GithubUser.GitHubUser(session['gh_token'])
    return render_template('page/profile.html',
                           img_src=api.prof_img(),
                           user_name=api.user_name(),
                           user_site=api.user_site())


#### error page ####
## 에러 페이지
@app.errorhandler(404)
def err_404(error):
    return render_template('page/error/4XX/404.html')


@app.errorhandler(403)
def err_404(error):
    return render_template('page/error/4XX/403.html')


@app.errorhandler(408)
def err_404(error):
    return render_template('page/error/4XX/408.html')


@app.errorhandler(400)
def err_404(error):
    return render_template('page/error/4XX/400.html')


@app.errorhandler(404)
def err_404(error):
    return render_template('page/error/4XX/404.html')


@app.errorhandler(500)
def err_404(error):
    return render_template('page/error/5XX/500.html')


@app.errorhandler(502)
def err_404(error):
    return render_template('page/error/5XX/502.html')


@app.errorhandler(503)
def err_404(error):
    return render_template('page/error/5XX/503.html')


@app.errorhandler(504)
def err_404(error):
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
    # session['temp'] = 4
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


## 부모창 새로고침, 현재창 닫기
@app.route('/auth/login_success')
def login_success():
    return '<head></head><body><script>opener.location.reload();close();</script></body>'


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
    gh = GithubUser.GitHubUser(session['gh_token'])
    return gh.repo_list_json()

if __name__ == '__main__':
    app.run()

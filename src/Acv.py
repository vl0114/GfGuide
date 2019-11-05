import requests
from src import db

funcs = [lambda name, token: c1(name, token), lambda name, token: c2(name, token)]


def c1(user_name, token):
    if has_repo(token, user_name, 'Gh-Test'):
        if has_readme(token, user_name, 'Gh-Test'):
            return has_any_file(token, user_name, 'Gh-Test')
    return False


def c2(user_name, token):
    if has_repo(token, user_name, 'Gh-Test'):
        if has_file(token, user_name, 'Gh-Test', 'README.md', branch_name='hotfix'):
            return has_any_file(token, user_name, 'Gh-Test', branch_name='hotfix')
    return False


def chk(uid: int, rid: int, gh_token: str):
    q = db.psql2()
    user_name = q.get(f'select gh_login from gh_user_caching where ghid = (select ghid from guser where uid = {uid})')
    f = funcs[int(rid) - 1]
    return f(user_name[0][0], gh_token)


def has_repo(token, user_name, repo_name):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'token ' + token}
    request = requests.request('GET', url=f'https://api.github.com/users/{user_name}/repos', headers=headers)
    try:
        r = request.json()
        for i in r:
            if i['name'] == repo_name:
                return True
    except:
        return False
    return False


def has_readme(token, user_name, repo_name):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'token ' + token}
    request = requests.request('GET', url=f'https://api.github.com/repos/{user_name}/{repo_name}/readme', headers=headers)
    try:
        r = request.json()

        if r['name'] == 'README.md':
            return True
    except:
        return False
    return False


def has_branch(token, user_name, repo_name, branch_name):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'token ' + token}
    request = requests.request('GET', url=f'https://api.github.com/repos/{user_name}/{repo_name}/branches', headers=headers)
    try:
        r = request.json()
        for i in r:
            if i['name'] == branch_name:
                return True
    except:
        return False
    return False


def has_file(token, user_name, repo_name, file_name, branch_name='master', path=''):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'token ' + token}
    request = requests.request('GET',
                               url=f'https://api.github.com/repos/{user_name}/{repo_name}/contents/{path}?ref={branch_name}', headers=headers)
    try:
        r = request.json()
        for i in r:
            if i['name'] == file_name:
                return True
    except:
        return False
    return False


def has_any_file(token, user_name, repo_name, branch_name='master', path=''):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'token ' + token}
    request = requests.request('GET',
                               url=f'https://api.github.com/repos/{user_name}/{repo_name}/contents/{path}?ref={branch_name}', headers=headers)
    try:
        r = request.json()
        for i in r:
            if 'name' in i:
                if i['name'] != 'README.md':
                    return True
    except:
        return False
    return False
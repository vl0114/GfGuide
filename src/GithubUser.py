## GitHub 데이터를 케싱, 가공하는 모듈
## DB 혹은 메모리에 케싱된다


from . import GitHubAPI, gh_db
import json, re, datetime
from . import utils

'''
ret['id'],
ret['login'],
ret['html_url'],
ret['name'],
ret['company'],
ret['blog'],
ret['location'],
ret['email'],
ret['public_repos'],
ret['public_gists'],
ret['followers'],
ret['following'],
ret['created']
ret['updated']
ret['created_this']
ret['updated_this']
'''

class GitHubUser:
    def __init__(self, token):
        self.gapi = GitHubAPI.GitHubAPI(token)
        self.gapi.requestUser()
        self.user_dict = self.gapi.getUser()
        self.gh_id = self.user_dict['id']
        self.user_db = gh_db.guser(self.gh_id)

    def set_token(self, token: str):
        self.gapi = GitHubAPI.GitHubAPI(token)

    def update_db(self):
        self.gapi.requestUser()
        self.user_dict = self.gapi.getUser()
        self.user_db.update_user_cache(self.user_dict)

    def get_db(self):
        self.user_db.request_user_cache()
        self.user_dict = self.user_db.user_cache

    def user_login(self):
        self.user_db.registe_user_data()
        self.user_db.update_user_cache(self.user_dict)

    def prof_img(self):
        uid = self.user_db.user_cache['id']
        return 'https://avatars0.githubusercontent.com/u/{}'.format(uid)

    def user_name(self):
        return self.user_db.user_cache['login']

    def user_site(self):
        return self.user_db.user_cache['html_url']

    def refresh_user_data(self):
        self.user_db.get_user_by_gh_id()

    def get_uid(self):
        return self.user_db.user_data['uid']


class GitHubRepo:
    def __init__(self, token, uid):
        self.repo_db = gh_db.grepo(token, uid)
        self.repo_db.get_from_db()

    def refresh_repos(self):
        self.repo_db.request_repo()
        self.repo_db.put_db()

    def get_repos_json(self):
        return json.dumps(self.repo_db.repo_list)


class Post:
    def __init__(self):
        self.pid = -1
        self.post_db = gh_db.post()

    def set(self, pid):
        self.pid = pid

    def create(self):
        #self.post_db.new
        pass

    def search(self, title: str):
        return json.dumps(self.post_db.search(title))

    def rm(self):
        self.post_db.rm(self.pid)

    def get_post(self):
        r = self.post_db.get(self.pid)
        c = r.copy()
        for i in r.keys():
            if isinstance(r[i], datetime.datetime):
                c[i] = str(r[i])
        return json.dumps(c)


class Gallery:
    def __init__(self):
        self.gid = -1
        self.gall_db = gh_db.gallery()

    def create(self, title: str, g_info: str, r_op: int = 0, w_op: int = 0):
        self.gall_db.new(title, g_info)
        r = self.gall_db.search_title_(title)
        self.gid = r['gid']

    def set(self, gid: int):
        self.gid = gid

    def search(self, title: str):
        r = self.gall_db.search_title(title)
        return json.dumps(r)

    def search_id(self, id: int):
        r = self.gall_db.search(id)
        return json.dumps(r)

    def rm(self):
        self.gall_db.rm(self.gid)

    def get_list(self):
        return json.dumps(self.gall_db.get_list())

    def post_list(self):
        r = self.gall_db.post_list(self.gid)
        l = self.gall_db.search(self.gid)
        l['posts'] = r
        return json.dumps(l)

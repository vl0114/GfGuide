# db sql 구문을 축약한 모듈

# sql injection 구문이 없음을 전제로 사용 해야함

from . import db, GitHubAPI
import datetime

class gallery:  # 겔러리
    def __init__(self):
        self.psql = db.psql2()
        self.pq = db.Query()

    def new(self, title: str, ginfo: str):
        gallery_data = dict()
        gallery_data['title'] = title
        gallery_data['ginfo'] = ginfo
        self.psql.send(self.pq.dict_to_insert(gallery_data, 'gallery'))

    def search(self, gid: int):
        ret = self.psql.get(
            self.pq.dict_to_select(None, 'gallery', ['gid', 'title', 'ginfo', 'created', 'r_op', 'w_op'],
                                   where=f"gid = '{gid}'"))
        r = dict(ret[0])
        c = r.copy()
        for i in r.keys():
            if isinstance(r[i], datetime.datetime):
                c[i] = str(r[i])
        return c

    def search_title(self, title: str):
        ret = self.psql.get(
            self.pq.dict_to_select(None, 'gallery', ['gid', 'title', 'ginfo', 'created', 'r_op', 'w_op'],
                                   where=f"title like '%{title}%'"))
        glist = list()
        for i in ret:
            glist.append(dict(i))

        return glist

    def search_title_(self, title: str):
        ret = self.psql.get(
            self.pq.dict_to_select(None, 'gallery', ['gid', 'title', 'ginfo', 'created', 'r_op', 'w_op'],
                                   where=f"title = '{title}'"))

        return dict(ret[0])

    def rm(self, gid):
        self.psql.send(f'delete from gallery where gid = {gid}')

    def modify(self, gid: int, title: str = None, ginfo: str = None):
        if title is None and ginfo is None:
            return
        q = "update gallery set "
        if title is not None:
            q = q + f"title = '{title}' "
        if ginfo is not None:
            q = q + f", ginfo = '{ginfo}'"
        q = q + f' where gid = {gid}'
        self.psql.send(q)
        self.psql.commit()

    def get_list(self):
        l = self.psql.get(self.pq.dict_to_select(None, 'gallery', ['gid', 'title']))
        r = list()
        for i in l:
            r.append({'gid': i[0], 'title': i[1]})
        return r

    def post_list(self, gid: int):
        ll = self.psql.get(self.pq.dict_to_select(None, 'post', ['pid', 'title'], f'gid = {gid}'))
        x = list()
        for i in ll:
            x.append({'pid': i[0], 'title': i[1]})
        return x


class post:  # 포스트
    def __init__(self):
        self.psql = db.psql2()
        self.pq = db.Query()

    def new(self, gid: int, title: str, main_text: str, render_type: str, writer: int):
        post_content = dict()
        post_content['title'] = title
        post_content['contents'] = main_text
        post_content['writer'] = writer
        if render_type == 'md':
            post_content['render_type'] = 1
        elif render_type == 'html':
            post_content['render_type'] = 2
        else:
            post_content['render_type'] = 0

        self.psql.send(self.pq.dict_to_insert(post_content, 'post'))

    def search(self, title: str):
        ret = self.psql.get(self.pq.dict_to_select(None, 'post', ['pid', 'title'],
                                                   where=f"title like '%{title}%'"))
        pid_list = list()
        for i in ret:
            pid_list.append({'pid': i[0], 'title': i[1]})
        return pid_list

    def rm(self, pid: int):
        self.psql.send(f'delete from post where pid = {pid}')

    def modify(self, title: str, main_text: str, render_type: str, writer: int):
        self.post_content['title'] = title
        self.post_content['contents'] = main_text
        self.post_content['writer'] = writer
        if render_type == 'md':
            self.post_content['render_type'] = 1
        elif render_type == 'html':
            self.post_content['render_type'] = 2
        else:
            self.post_content['render_type'] = 0
        q = self.pq.dict_to_update(self.post_content, 'post', f'pid = {self.post_content["pid"]}')
        self.psql.send(q)
        self.psql.commit()

    def get(self, pid):
        return self.psql.get(self.pq.dict_to_select(None, 'post', ['pid', 'gid', 'title', 'contents',
                                                                   'upload_date',
                                                                   'recent_date', 'r_op', 'w_op',
                                                                   'writer, render_type', 'views'],
                                                    f'pid = {pid}'
                                                    ))[0]

    def get_title(self, pid):
        return self.psql.get(f"select title from post where pid = {pid}")


'''
self.user_data['uid']     = 
self.user_data['registe'] =
self.user_data['code']    = 
self.user_data['opl']     = 
self.user_data['gh_id']   = 
self.user_data['status']  = 
'''
'''
ret['id'] = res1[0]
ret['login'] = res1[1]
ret['html_url'] = res1[2]
ret['name'] = res1[3]
ret['company'] = res[4]
ret['blog'] = res[5]
ret['location'] = res[6]
ret['email'] = res[7]
ret['public_repos'] = res[8]
ret['public_gists'] = res[9]
ret['followers'] = res[10]
ret['following'] = res[11]
'''


class grepo:  # 리포지토리
    def __init__(self, token: str, uid: int):
        self.uid = uid
        self.token = token
        self.repo_list = list()
        self.psql = db.psql2()
        print('>>>>>>>', uid)
        self.gh_id = (self.psql.get('select ghid from guser where  uid = {}'.format(uid)))[0]['ghid']
        self.pq = db.Query()

    # API -> 메모리
    def request_repo(self):
        req = GitHubAPI.GitHubAPI(self.token)
        req.requestRepo()
        d = req.repo_dict
        self.repo_list = list()

        for repo in d:
            copy_repo = dict()
            copy_repo['repo_id'] = repo['id']
            copy_repo['full_name'] = repo['full_name']
            copy_repo['is_private'] = repo['private']
            copy_repo['repo_name'] = repo['name']
            copy_repo['description'] = repo['description']
            copy_repo['html_url'] = 'https://github.com/' + repo['full_name']
            copy_repo['is_fork'] = repo['fork']
            copy_repo['git_url'] = repo['git_url']
            copy_repo['ssh_url'] = repo['ssh_url']
            copy_repo['clone_url'] = repo['clone_url']
            copy_repo['mirror_url'] = repo['mirror_url']
            copy_repo['lang'] = repo['language'] if repo["language"] is not None else 'Unknown'
            copy_repo['fork_count'] = repo['forks_count']
            copy_repo['star_count'] = repo['stargazers_count']
            copy_repo['watcher_count'] = repo['watchers_count']
            copy_repo['size'] = repo['size']
            copy_repo['default_branch'] = repo['default_branch']
            copy_repo['open_issue_count'] = repo['open_issues_count']

            copy_repo["has_issue"] = repo["has_issues"]
            copy_repo["has_project"] = repo["has_projects"]
            copy_repo["has_wiki"] = repo["has_wiki"]
            copy_repo["has_page"] = repo["has_pages"]
            copy_repo["has_download"] = repo["has_downloads"]
            copy_repo["archived"] = repo["archived"]
            copy_repo["disabled"] = repo["disabled"]
            copy_repo["pushed_at"] = repo["pushed_at"]
            copy_repo["created_at"] = repo["created_at"]
            copy_repo["updated_at"] = repo["updated_at"]
            copy_repo['owner_id'] = repo['owner']['id']
            copy_repo['per_admin'] = repo['permissions']['admin']
            copy_repo['per_push'] = repo['permissions']['push']
            copy_repo['per_pull'] = repo['permissions']['pull']

            copy_repo['license'] = repo["license"]["key"] if repo["license"] is not None else 'None'
            copy_repo['uid'] = self.uid

            self.repo_list.append(copy_repo)

    # db -> 메모리
    def get_from_db(self):
        if self.psql.get(f"select count(*) from gh_repo_caching where uid = {self.uid}")[0][0] == 0:
            self.request_repo()
            self.put_db()

        self.repo_list = list()
        r = self.psql.get('select * from gh_repo_caching where uid = {}'.format(self.uid))
        for i in r:
            av = dict(i)
            av.pop('pushed_at')
            av.pop('created_at')
            av.pop('updated_at')
            # av['license'] = av["license"]["key"] if av["license"] is not None else 'None'

            self.repo_list.append(av)

    # 메모리 -> db if 메모리 is None API -> 메모리 -> db
    def put_db(self):
        for i in self.repo_list:
            if self.psql.get(f"select count(*) from gh_repo_caching where repo_id = {i['repo_id']}")[0][0] == 0:
                self.psql.send(self.pq.dict_to_insert(i, 'gh_repo_caching'))
                self.psql.commit()
            else:
                self.psql.send(self.pq.dict_to_update(i, 'gh_repo_caching', f'repo_id = {i["repo_id"]}'))
                self.psql.commit()

        repoc = self.psql.get(f"select repo_id from gh_repo_caching where uid = {self.uid}")
        for i in repoc:

            is_contain = False
            for j in self.repo_list:
                if i[0] == j['repo_id']:
                    is_contain = True

            if not is_contain:
                self.psql.send(f"delete from gh_repo_caching where repo_id = {i[0]}")


class guser:  # 유저
    def __init__(self, gh_id: int):
        self.gh_id = gh_id

        # using in guser
        self.user_data = dict()
        self.user_data['uid'] = -1  # 관리용 user id
        self.user_data['registe'] = ''  # 시스템 등록날
        self.user_data['code'] = 0  # code
        self.user_data['opl'] = 0  # 관리자 레벨
        self.user_data['gh_id'] = gh_id  # github 고유 id
        self.user_data['status'] = 0  # 계정 상태         # 0:보통, -1:탈퇴, -2:임시조치

        # using in gh_user_cache
        self.user_cache = dict()
        self.user_cache['id'] = gh_id  # github id
        self.user_cache['login'] = ''  # github 이름
        self.user_cache['html_url'] = ''  # github page
        self.user_cache['name'] = ''  # 이름
        self.user_cache['company'] = ''  # 회사
        self.user_cache['blog'] = ''  # 블로그
        self.user_cache['location'] = ''  # 장소
        self.user_cache['email'] = ''  # 이메일
        self.user_cache['public_repos'] = 0  # public repo 수
        self.user_cache['public_gists'] = 0  # public gist 수
        self.user_cache['followers'] = 0  # 팔로워수
        self.user_cache['following'] = 0  # 팔로우수

        self.psql = db.psql()

    # 새로운 유저 등록 메모리 -> db
    def registe_user_data(self):
        if (self.psql.get(f"select count(*) from guser where ghid = {self.gh_id}"))[0][0] == 0:
            self.psql.send(f"insert into guser (ghid) values ({self.gh_id})")
            self.psql.commit()

    # tuple -> dict
    def set_user_data(self, res: tuple):  # uid, registe_date, code, opl, ghid, status
        self.user_data['uid'] = res[0]
        self.user_data['registe'] = res[1]
        self.user_data['code'] = res[2]
        self.user_data['opl'] = res[3]
        self.user_data['gh_id'] = res[4]
        self.user_data['status'] = res[5]

    # db -> 메모리
    def get_user_by_gh_id(self):
        x = self.psql.get(f"select uid, registe_date, code, opl, ghid, status from guser "
                          f"where ghid = {self.gh_id}")
        res = x[0]
        self.set_user_data(res)

    # user status value set -1
    def draw_user(self):
        self.psql.send(f"update guser set status = -1 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['status'] = -1

    # user status value set -2
    def rest_user(self):
        self.psql.send(f"update guser set status = -2 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['status'] = -2

    # user opl value set 30
    def promote_admin(self):
        self.psql.send(f"update guser set opl = 30 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['opl'] = 30

    # user opl value set 0
    def demote_general(self):
        self.psql.send(f"update guser set opl = 0 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['opl'] = 0

    ########

    def set_user_cache(self,
                       res: tuple):  # ghid, gh_login, html_url, user_name, company, blog, loc, email, public_repos, public_gists, followers, followings
        self.user_cache['id'] = res[0]
        self.user_cache['login'] = res[1]
        self.user_cache['html_url'] = res[2]
        self.user_cache['name'] = res[3]
        self.user_cache['company'] = res[4]
        self.user_cache['blog'] = res[5]
        self.user_cache['location'] = res[6]
        self.user_cache['email'] = res[7]
        self.user_cache['public_repos'] = res[8]
        self.user_cache['public_gists'] = res[9]
        self.user_cache['followers'] = res[10]
        self.user_cache['following'] = res[11]

    # API -> memory
    def request_user_cache(self):
        res = self.psql.get(f"select ghid, gh_login, html_url, user_name, company, blog, loc, email, public_repos,"
                            f" public_gists, followers, followings from gh_user_caching "
                            f"where ghid = {self.user_cache['id']}")
        res1 = res[0]
        self.set_user_cache(res1)

    # memory -> DB
    def update_user_cache(self, user_dict: dict):
        self.user_cache = user_dict
        if self.psql.get(f"select count(*) from gh_user_caching where ghid = {self.user_cache['id']}")[0][0] == 0:
            self.psql.send(
                "insert into gh_user_caching (ghid, gh_login, html_url, user_name, company,"
                "blog, loc, email, public_repos, public_gists, followers, followings) values"
                "({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {})"
                    .format(self.user_cache['id'],
                            self.user_cache['login'],
                            self.user_cache['html_url'],
                            self.user_cache['name'],
                            self.user_cache['company'],
                            self.user_cache['blog'],
                            self.user_cache['location'],
                            self.user_cache['email'],
                            self.user_cache['public_repos'],
                            self.user_cache['public_gists'],
                            self.user_cache['followers'],
                            self.user_cache['following']))
            self.psql.commit()
        else:
            self.psql.send(
                "update gh_user_caching set gh_login='{}', html_url='{}', user_name='{}', company='{}',"
                "blog='{}', loc='{}', email='{}', public_repos={}, public_gists={}, "
                "followers={}, followings={}, updated_this=now() where ghid={}"
                    .format(self.user_cache['login'],
                            self.user_cache['html_url'],
                            self.user_cache['name'],
                            self.user_cache['company'],
                            self.user_cache['blog'],
                            self.user_cache['location'],
                            self.user_cache['email'],
                            self.user_cache['public_repos'],
                            self.user_cache['public_gists'],
                            self.user_cache['followers'],
                            self.user_cache['following'],
                            self.user_cache['id']))
            self.psql.commit()

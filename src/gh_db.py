# db sql 구문을 축약한 모듈

# sql injection 구문이 없음을 전제로 사용 해야함

from . import db, GitHubAPI


class gallery:  # 겔러리
    def __init__(self):
        self.psql = db.psql()
        self.gid = -1  # gallery id
        self.title = ''  # 제목
        self.ginfo = ''  # 겔러리 정보
        # created
        self.r_op = 0  # 읽기권한
        self.w_op = 0  # 쓰기권한
        self.code = 0  # 기타 코드

    def registe_gallery(self, title: str, info: str = ''):
        self.psql.send("insert into gallery(title, ginfo) VALUES ('{}', '{}')"
                       .format(title, info))
        r = self.psql.get("select gid from gallery where title = '{}'".format(title))
        self.gid = (r[0][0])
        return self.gid

    def get_gid(self, title: str):
        r = self.psql.get("select gid from gallery where title = '{}'".format(title))
        self.gid = (r[0][0])
        return self.gid

    def add_post(self, title: str, contents: str, writer: int):
        self.psql.send("insert into post(gid, contents, title, writer) values ({}, '{}', '{}', {})"
                       .format(self.gid, contents, title, writer))
        self.psql.commit()

    def modify_post(self, pid: int, title: str, contents: str):
        self.psql.send("update post set contents = '{}', title = '{}' where pid = {}"
                       .format(contents, title, pid))

    def get_post(self, pid: int):
        return self.psql.get("select title, contents, upload_date, recent_date from post where pid = {}".format(pid))

    def get_all_post_from_gallery(self):
        return self.psql.get(
            "select title, contents, upload_date, recent_date from post where gid = {}".format(self.gid))


class post:  # 포스트
    def __init__(self):
        self.psql = db.psql()
        self.pid = -1  # post id
        self.gid = -1
        self.contents = ''  # 본문
        self.title = ''  # 제목
        # upload_date
        # recent_date
        self.code = 0  # 기타 코드
        self.r_op = 0  # 읽기 권한 레벨
        self.views = 0
        self.w_op = 0  # 쓰기(편집) 권한 레벨
        self.writer = 0  # 작성자 uid


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
            copy_repo['full_name'] = repo['full_name']
            copy_repo['is_fork'] = repo['fork']
            copy_repo['git_url'] = repo['git_url']
            copy_repo['ssh_url'] = repo['ssh_url']
            copy_repo['clone_url'] = repo['clone_url']
            copy_repo['mirror_url'] = repo['mirror_url']
            copy_repo['lang'] = repo['language']
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

            copy_repo['license'] = repo["license"]['key']
            copy_repo['uid'] = self.uid

            self.repo_list.append(copy_repo)


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
            self.repo_list.append(av)

    def put_db(self):
        for i in self.repo_list:
            if self.psql.get(f"select count(*) from gh_repo_caching where repo_id = {i['repo_id']}")[0][0] == 0:
                self.psql.send(self.pq.dict_to_insert(i, 'gh_repo_caching'))
                self.psql.commit()
            else:
                self.psql.send(self.pq.dict_to_update(i, 'gh_repo_caching', f'repo_id = {i["repo_id"]}'))
                self.psql.commit()

class guser:  # 유저
    def __init__(self, gh_id: int):
        self.gh_id = gh_id

        # using in guser
        self.user_data = dict()
        self.user_data['uid'] = -1       # 관리용 user id
        self.user_data['registe'] = ''   # 시스템 등록날
        self.user_data['code'] = 0       # code
        self.user_data['opl'] = 0        # 관리자 레벨
        self.user_data['gh_id'] = gh_id  # github 고유 id
        self.user_data['status'] = 0     # 계정 상태         # 0:보통, -1:탈퇴, -2:임시조치

        # using in gh_user_cache
        self.user_cache = dict()
        self.user_cache['id'] = gh_id           # github id
        self.user_cache['login'] = ''           # github 이름
        self.user_cache['html_url'] = ''        # github page
        self.user_cache['name'] = ''            # 이름
        self.user_cache['company'] = ''         # 회사
        self.user_cache['blog'] = ''            # 블로그
        self.user_cache['location'] = ''        # 장소
        self.user_cache['email'] = ''           # 이메일
        self.user_cache['public_repos'] = 0     # public repo 수
        self.user_cache['public_gists'] = 0     # public gist 수
        self.user_cache['followers'] = 0        # 팔로워수
        self.user_cache['following'] = 0        # 팔로우수

        self.psql = db.psql()

    def registe_user_data(self):
        if (self.psql.get(f"select count(*) from guser where ghid = {self.gh_id}"))[0][0] == 0:
            self.psql.send(f"insert into guser (ghid) values ({self.gh_id})")
            self.psql.commit()

    def set_user_data(self, res: tuple): # uid, registe_date, code, opl, ghid, status
        self.user_data['uid'] = res[0]
        self.user_data['registe'] = res[1]
        self.user_data['code'] = res[2]
        self.user_data['opl'] = res[3]
        self.user_data['gh_id'] = res[4]
        self.user_data['status'] = res[5]

    def get_user_by_gh_id(self):
        x = self.psql.get(f"select uid, registe_date, code, opl, ghid, status from guser "
                          f"where ghid = {self.gh_id}")
        res = x[0]
        self.set_user_data(res)

    def draw_user(self):
        self.psql.send(f"update guser set status = -1 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['status'] = -1

    def rest_user(self):
        self.psql.send(f"update guser set status = -2 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['status'] = -2

    def promote_admin(self):
        self.psql.send(f"update guser set opl = 30 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['opl'] = 30

    def demote_general(self):
        self.psql.send(f"update guser set opl = 0 where uid = {self.user_data['uid']}")
        self.psql.commit()
        self.user_data['opl'] = 0

    ########

    def set_user_cache(self, res: tuple): # ghid, gh_login, html_url, user_name, company, blog, loc, email, public_repos, public_gists, followers, followings
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

    def request_user_cache(self):
        res = self.psql.get(f"select ghid, gh_login, html_url, user_name, company, blog, loc, email, public_repos,"
                            f" public_gists, followers, followings from gh_user_caching "
                            f"where ghid = {self.user_cache['id']}")
        res1 = res[0]
        self.set_user_cache(res1)

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


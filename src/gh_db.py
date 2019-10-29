# db sql 구문을 축약한 모듈

# sql injection 구문이 없음을 전제로 사용 해야함


from . import db


class gallery: # 겔러리
    def __init__(self):
        self.psql = db.psql()
        self.gid = -1       # gallery id
        self.title = ''     # 제목
        self.ginfo = ''     # 겔러리 정보
        # created
        self.r_op = 0       # 읽기권한
        self.w_op = 0       # 쓰기권한
        self.code = 0       # 기타 코드

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
        return self.psql.get("select title, contents, upload_date, recent_date from post where gid = {}".format(self.gid))


class post: # 포스트
    def __init__(self):
        self.psql = db.psql()
        self.pid = -1       # post id
        self.gid = -1
        self.contents = ''  # 본문
        self.title = ''     # 제목
        # upload_date
        # recent_date
        self.code = 0  # 기타 코드
        self.r_op = 0       # 읽기 권한 레벨
        self.views = 0
        self.w_op = 0       # 쓰기(편집) 권한 레벨
        self.writer = 0     # 작성자 uid


class guser: # 유저
    def __init__(self):
        self.psql = db.psql()
        self.uid = -1       # user id       # 수신x=-1
        self.gh_name = ''   # GitHub id
        self.gname = ''     # site name
        self.code = 0       # code          # 보통-0, 제한-1, 탈톼-2,
        self.opl = 0        # 권한 레벨      # 보통-0 ~ 30

    def registe_user(self, gh_name: str, gname: str):
        self.gh_name = gh_name
        self.gname = gname

        self.psql.send(f"insert into guser(gh_name, gname) values ('{gh_name}', '{gname}')")
        self.psql.commit()
        r = self.psql.get(f"select uid from guser where gh_name = '{gh_name}'")
        self.uid = r[0][0]
        self.code = 0
        self.opl = 0

    def get_user(self, gh_name: str):
        r = self.psql.get(f"select * from guser where gh_name = '{gh_name}'")
        self.uid = r[0][0]
        self.gh_name = r[0][1]
        self.gname = r[0][2]
        self.code = r[0][4]
        self.opl = r[0][5]

    def draw_user(self):
        self.psql.send(f"update guser set code = 2 where uid = {self.uid}")
        self.psql.commit()
        self.code = 2

    def rest_user(self):
        self.psql.send(f"update guser set code = 1 where uid = {self.uid}")
        self.psql.commit()
        self.code = 1

    def promote_admin(self):
        self.psql.send(f"update guser set opl = 30 where uid = {self.uid}")
        self.psql.commit()
        self.opl = 30

    def demote_general(self):
        self.psql.send(f"update guser set opl = 0 where uid = {self.uid}")
        self.psql.commit()
        self.opl = 0
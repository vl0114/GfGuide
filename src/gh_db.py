from . import db


class Gallery:
    def __init__(self):
        self.psql = db.psql()
        self.gid = -1
    '''
        pid         serial not null
            constraint post_pk
                primary key,
        gid         serial not null,
        contents    text,
        title       text,
        upload_date timestamp default now(),
        recent_date timestamp default now(),
        code        integer   default 0,
        op          integer   default 0,
        view        integer   default 0
    '''

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


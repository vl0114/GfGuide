## GitHub 데이터를 케싱, 가공하는 모듈
## DB 혹은 메모리에 케싱된다


from . import GitHubAPI
import json, re
from . import utils

class GitHubUser:

    def __init__(self, gh_token):
        self.gapi = GitHubAPI.GitHubAPI(gh_token)
        self.gapi.requestUser()
        self.gapi.requestRepo()
        self.token = gh_token

    def user_name(self):
        return self.gapi.getUser()['login']

    def prof_img(self):
        uid = self.gapi.getUser()['id']
        return 'https://avatars0.githubusercontent.com/u/{}'.format(uid)

    def user_site(self):
        return self.gapi.getUser()['html_url']

    def repo_list_json(self):
        #repo_dict = dict()
        repo_dict_list = json.loads(self.gapi.repo_json)
        copy_dict = dict()
        copy_dict_list = list()
        reg = re.compile('.*_url')

        for j in range(len(repo_dict_list)):
            for i in (repo_dict_list[j]).keys():
                if i in ["html_url", 'git_url', 'ssh_url', 'clone_url', 'svn_url', 'mirror_url']:
                    continue
                if reg.match(i) is None:
                    copy_dict[i] = repo_dict_list[j][i]
            copy_dict_list.append(copy_dict)
            copy_dict = dict()

        return json.dumps(copy_dict_list)



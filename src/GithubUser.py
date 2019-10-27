## GitHub 데이터를 케싱, 가공하는 모듈
## DB 혹은 메모리에 케싱된다


from . import GitHubAPI


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
        return self.gapi.repo_json



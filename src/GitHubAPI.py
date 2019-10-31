## GitHub API를 통해 실제로 데이터를 요청하는 모듈


import requests


class GitHubAPI:

    def __init__(self, gh_tk):
        self.token = gh_tk
        self.user_dict = None
        self.repo_dict = None

    def requestUser(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'token ' + self.token}
        request = requests.request('GET', url='https://api.github.com/user', headers=headers)
        self.user_dict = request.json()

    def getUser(self):
        return self.user_dict

    def requestRepo(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'token ' + self.token}
        request = requests.request('GET', url='https://api.github.com/user/repos', headers=headers)
        self.repo_dict = request.json()



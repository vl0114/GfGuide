## GitHub 인증을 담당하는 모듈


from . import Setting
import requests


class GHLogin:

    def __init__(self):
        pass

    @staticmethod
    def generate_gh_redirect_url(key: str):
        return "https://github.com/login/oauth/authorize?client_id={}&redirect_uri={}&state={}".format(Setting.Secret.ID, Setting.Page.Redirect, key)

    @staticmethod
    def request_token(code: str):
        param = {'code': code,
                 'client_secret': Setting.Secret.SECRET,
                 'client_id': Setting.Secret.ID}
        request = requests.post(url='https://github.com/login/oauth/access_token', params=param, headers={'Accept': 'application/json'})
        ret = request.json()
        token = ret['access_token']
        return token

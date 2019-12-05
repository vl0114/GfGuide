## SECRET KEY
프로젝트 구동에 필요한 암호(hash)들을 관리하는 파일 입니다.

- GitHub Api ID, Secret key
- Session 암호화 키
- 유저 데이터 암호화 키
- 데이타베이스
  * 호스트
  * 포트
  * DB
  * ID
  * PW
  

## 구조
/secret.py

```python3
class SECRET:
    def importSetting(self, path = './Setting.json'):
        j = open(path, 'r')


    GITHUB_CLIENT_ID = "GITHUB_CLIENT_ID"
    GITHUB_CLIENT_SECRET = "GITHUB_CLIENT_SECRET"
    SUPER_SECRET = 'FLASK_SUPER_SECRET'

    class DB:
        HOST = 'DATABASE_HOST'
        DB = 'DATABASE_NAME'
        USER = 'DATABASE_USER'
        PW = 'DATABASE_SECRET'
        PORT = 'DATABASE_PORT'
```

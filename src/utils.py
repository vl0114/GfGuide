import re, json


def filter_json_str_keys(json_str: str, regex: str, white_list: list):
    # repo_dict = dict()
    repo_dict = json.loads(json_str)
    copy_dict = dict()
    copy_dict_list = list()
    reg = re.compile(regex)
    if type(repo_dict) == type(dict()):
        for i in repo_dict.keys():
            if i in white_list:
                continue
            if reg.match(i) is None:
                copy_dict[i] = repo_dict[i]
        copy_dict_list.append(copy_dict)
        return json.dumps(copy_dict)

    elif type(repo_dict) == type(list()):
        copy_dict_list = list()
        for j in range(len(repo_dict)):
            for i in (repo_dict[j]).keys():
                if i in white_list:
                    continue
                if reg.match(i) is None:
                    copy_dict[i] = repo_dict[j][i]
            copy_dict_list.append(copy_dict)
            copy_dict = dict()
        return json.dumps(copy_dict_list)

    else:
        return None


def filter_json_dict_keys(json_dict, regex: str, white_list: list):
    # repo_dict = dict()
    repo_dict = json_dict
    copy_dict = dict()
    copy_dict_list = list()
    reg = re.compile(regex)
    if type(repo_dict) == type(dict()):
        for i in repo_dict.keys():
            if i in white_list:
                continue
            if reg.match(i) is None:
                copy_dict[i] = repo_dict[i]
        copy_dict_list.append(copy_dict)
        return copy_dict

    elif type(repo_dict) == type(list()):
        copy_dict_list = list()
        for j in range(len(repo_dict)):
            for i in (repo_dict[j]).keys():
                if i in white_list:
                    continue
                if reg.match(i) is None:
                    copy_dict[i] = repo_dict[j][i]
            copy_dict_list.append(copy_dict)
            copy_dict = dict()
        return copy_dict_list

    else:
        return None


# xss 공격 검사
def filter_xss(contents: str):
    pass


# sql injection 검사
def filter_sql_inj(contents: str):
    pass
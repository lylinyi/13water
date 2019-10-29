import requests
import json


def register(user, password):
    url = "http://www.revth.com:12300/auth/register2"
    form_data = {
        "username": user["username"],
        "password": user["password"],
        "student_number": password["student_number"],
        "student_password": password["student_password"]
    }
    headers = {
        "Content-Type": 'application/json',
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(form_data), verify=False)
    print(response.text)
    return response.json()["status"]


'''
{
  "status": 0,
  "data": {
    "id": 1000,
    "card": "*2 *3 *4 *5 *6 *7 *8 *9 *10 *J *Q *K *A"
  }
}
'''


def begin_game(token):
    url = "http://api.revth.com/game/open"
    headers = {
        "X-Auth-Token": token,
    }
    response = requests.post(url=url, headers=headers, verify=False).json()
    print("系统发牌,牌型:")
    card = response["data"]["card"]
    id = response["data"]["id"]
    print(card)
    return id, card


# 出牌
def play(id, cards, token):
    """
    :param cards: list of string
    """
    url = "http://api.revth.com/game/submit"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
    }
    form_data = {
        "id": id,
        "card": cards,
    }
    print("出牌结果:")
    print(json.dumps(form_data))
    response = requests.post(url=url, headers=headers, data=json.dumps(form_data), verify=False)

    if response.json()["status"] == 0:
        print("出牌成功")
        return 0
    print("出牌错误:")
    print(response.text)


def login(name,psw):
    url1 = "http://www.revth.com:12300/auth/login"
    # url2 = "http://www.revth.com:12300/auth/validate"
    headers1 = {
        "Content-Type": 'application/json',
    }
    form_data = {
        "username": name,
        "password": psw,
    }
    response = requests.post(url=url1, headers=headers1, data=json.dumps(form_data), verify=False)
    # print(response.text)
    print(response.json()["data"]["token"])
    re_js = response.json()
    if re_js["status"] == 0:
        return response.json()["data"]["token"]
    else:
        return re_js["status"]


def get_detail(token, id):
    url = "http://api.revth.com/history/{}".format(id)
    header = {
        "X-Auth-Token": token,
    }
    response = requests.get(url, headers=header)
    print(response.text)
    re_js = response.json()
    if re_js["status"] == 0:
        return re_js
    else:
        return False


def get_game_list(token):
    url = "http://api.revth.com/history"
    header = {
        "X-Auth-Token": token,
    }
    params = {'player_id': '25', 'limit': '10', 'page': 0}
    response = requests.get(url, headers=header, params=params)

    re_js = response.json()

    print(re_js)
    if re_js["status"] == 0:

        return re_js
    else:
        return False


def get_ranking():
    url = "http://api.revth.com/rank"
    response = requests.get(url)
    re_js = response.json()
    for i in re_js:
        print(i["name"])
        print(i["score"])
        # print(i["player_id"])

    # js["name"],js["score"],js["player_id"]
    return re_js



if __name__ == '__main__':
    # register(user, jwc)
    token = login()
    get_game_list(token)
    get_ranking()
    get_detail(token, 60600)

# 38b250a2-94e4-4afe-a8dd-1df58fd73726

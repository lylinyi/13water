import api
import ai
import time

toeken = ""
while True:
    token = api.login()
    while True:
        try:
            game_id, card = api.begin_game(token)
            res = ai.solve(card)
            api.play(game_id, res, token)
            print("--------比赛结果---------")
            time.sleep(1)
            # api.get_detail(token,game_id)
            api.get_game_list(token)
            print("-------------------")
            print()
        except:
            break

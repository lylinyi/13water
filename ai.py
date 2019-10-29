import re
import json
import api
import pattern
import weight
import itertools
import time

color_map = {'#': 0, '*': 1, '&': 2, '$': 3}
number_map = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
              'Q': 12, 'K': 13, 'A': 14}
colors = ['#', '*', '&', '$']
numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


# 结构[(1,2)]
def to_card(cards):
    card_list = re.findall(r"[*&$#]\d+|[*&$#]\w", cards)
    fmt_card_list = []

    for card in card_list:
        a = color_map[card[0]]
        b = number_map[card[1:]]
        fmt_card_list.append((a, b))
    return fmt_card_list


# 参数为按墩序的列表
def to_res(card):
    card_list = []
    c1 = ""
    c2 = ""
    c3 = ""
    for i in range(0, len(card)):
        if i < 3:
            if i != 2:
                c1 += colors[card[i][0]] + numbers[card[i][1] - 2] + " "
            else:
                c1 += colors[card[i][0]] + numbers[card[i][1] - 2]
        elif i < 8:
            if i != 7:
                c2 += colors[card[i][0]] + numbers[card[i][1] - 2] + " "
            else:
                c2 += colors[card[i][0]] + numbers[card[i][1] - 2]
        else:
            if i != 12:

                c3 += colors[card[i][0]] + numbers[card[i][1] - 2] + " "
            else:
                c3 += colors[card[i][0]] + numbers[card[i][1] - 2]
    card_list.append(c1)
    card_list.append(c2)
    card_list.append(c3)
    return card_list


def get_weight(pos, card):
    c = pattern.Card(card)
    # 同花顺 >炸弹 >葫芦 >同花 >顺子 >三条 >二对 >一对 >散牌
    num = 0
    if len(card) == 5:
        num = c.is_TongHuaShun()
        if num:
            return (9, num, weight.straight_flush[pos][num - 1])
        num = c.is_ZhaDan()
        if num:
            return (8, num, weight.four_of_a_kind[pos][num - 1])
        num = c.is_HuLu()
        if num:
            return (7, num, weight.full_house[pos][num - 1])
        num = c.is_TongHua()
        if num:
            return (6, num, weight.flush[pos][num - 1])
        num = c.is_straight()
        if num:
            return (5, num, weight.straight[pos][num - 1])
        num = c.is_triple()
        if num:
            return (4, num, weight.triple[pos][num - 1])
        num = c.is_tcpair()
        if num:
            return (3, num, weight.two_cpair[pos][num - 1])

        num = c.is_tpair()
        if num:
            return (2, num, weight.two_pair[pos][num - 1])
        num = c.is_pair()
        if num:
            return (1, num, weight.one_pair[pos][num - 1])
        num = c.is_junk()
        if num:
            return (0, num, weight.junk[pos][num - 1])
    elif len(card) == 3:
        num = c.is_triple()
        if num:
            return (4, num, weight.triple[pos][num - 1])
        if num:
            return (2, num, weight.two_pair[pos][num - 1])
        num = c.is_pair()
        if num:
            return (1, num, weight.one_pair[pos][num - 1])
        num = c.is_junk()
        if num:
            return (0, num, weight.junk[pos][num - 1])


def solve(card):
    """
    :param card13: 服务器返回的字符串列表
    :return: 符合参数格式的字符串列表
    """
    card = to_card(card)
    cnt = 0
    card_list = card
    # FLAG=0
    # print(card)
    card13 = pattern.Card(card)

    # 特殊牌型不判断
    # if card13.is_Dragon() or card13.is_tttt() or card13.is_12Huang() or card13.is_all_big() \
    #         or card13.is_same_color() or card13.is_3tonghuashun() or card13.is_3straight() \
    #         or card13.is_3zhadan() or card13.is_all_small() or card13.is_tcolor():
    #     FLAG=1
    #     print("special")
    #     ans = card_list
    max = -1
    ans = []
    iterator = itertools.combinations(card_list, 5)
    for iter in iterator:
        card1 = list(iter)
        tmp_card = card[:]
        for c in card1:
            tmp_card.remove(c)
        iterator2 = itertools.combinations(tmp_card, 5)
        for iter2 in iterator2:
            card2 = list(iter2)
            tmp_card2 = tmp_card[:]  # 八张
            for c in card2:
                tmp_card2.remove(c)
            card3 = tmp_card2
            n1 = get_weight(2, card1)
            n2 = get_weight(1, card2)
            n3 = get_weight(0, card3)

            if (n1 > n2 and n2 > n3):
                # if FLAG==1:
                #     ans = card3 + card2 + card1
                #     return ans
                if (n1[2] + n2[2] + n3[2] > max):
                    ans = card3 + card2 + card1
                    max = n1[2] + n2[2] + n3[2]
                    # print("----maxnum----:"+str(max)+"="+str(n1[2])+"+"+str(n2[2])+"+"+str(n3[2]))
    # [()]
    ans = to_res(ans)
    return ans


def main():
    card = "*5 &Q &7 $3 *A #3 &6 $9 $6 *10 *3 $J &5"

    # # print(get_weight(1, to_card("&2 #3 $6 $Q &Q")))
    # res = solve(card)
    # print(res)

    token=api.login()
    game_id, card = api.begin_game(token)
    res = solve(card)
    api.play(game_id, res, token)
    print("--------比赛结果---------")

    time.sleep(2)
    api.get_game_list(token)
    # api.get_detail(token, game_id)

    print("-------------------")
    print()


if __name__ == '__main__':
    main()

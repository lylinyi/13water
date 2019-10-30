# 普通牌型
def takeSecond(elem):
    return elem[1]


class Card:
    # [0,0,1,2...]从2开始

    # card参数格式[(1,1),(2,3)]
    def __init__(self, card):
        self.card = card
        self.card.sort(key=takeSecond)
        self.cnt_num = [0 for i in range(0, 15)]
        self.cnt_color = [0 for i in range(0, 4)]
        for c in card:
            self.cnt_num[c[1]] += 1
            self.cnt_color[c[0]] += 1
        if len(card)>5:
            print("-------------牌型--------------------")
            print(card)
            print(self.cnt_num)
            print(self.cnt_color)
            print("-------------------------------------------")
    # -----------普通牌型-------------------

    def is_tcpair(self):
        cnt = 0
        nums = []
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                cnt += 1
                nums.append(i)
        if len(nums) == 2 and abs(nums[0] - nums[1]) == 1:
            return max(nums)
        else:
            return False

    def is_junk(self):
        return max(self.card, key=takeSecond)[1]

    # 一对
    def is_pair(self):
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                return i
        return False

    # 两对
    def is_tpair(self):
        cnt = 0
        max_num = -1
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                cnt += 1
                max_num = (i if (i > max_num) else max_num)
        if cnt == 2:
            return max_num
        return False

    # 先判断葫芦,避免判断成三条
    def is_triple(self):
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] == 3:
                return i
        return False

    # 顺子
    def is_straight(self):
        for i in range(len(self.card) - 1):

            if self.card[i][1] + 1 != self.card[i + 1][1]:
                return False
        return self.card[len(self.card) - 1][1]

    # 判断五张牌的同花
    def is_TongHua(self):
        for i in self.cnt_color:
            if i == 5:
                return max(self.card, key=takeSecond)[1]
        return False

    # 葫芦
    def is_HuLu(self):
        two = False
        three = False
        index = 0
        for i in range(0, len(self.cnt_num)):
            if self.cnt_num[i] == 2:
                two = True
            if self.cnt_num[i] == 3:
                index = i
                three = True
        if three and two:
            return index
        else:
            return False

    # 炸弹
    def is_ZhaDan(self):
        for i in range(len(self.cnt_num)):
            if self.cnt_num[i] >= 4:
                return i
        return False

    # 同花顺
    def is_TongHuaShun(self):
        return self.is_TongHua() and self.is_straight()

    # ----------------特殊牌型----------------

    

list = [(1, 2), (1, 3), (1, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13)]
if __name__ == '__main__':
    c = Card(list)

    print(c.is_3tonghuashun())
